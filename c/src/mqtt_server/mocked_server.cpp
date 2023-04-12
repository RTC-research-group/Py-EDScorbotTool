#include <signal.h>
#include <iostream>
#include <string>
#include <thread>
#include <unistd.h>
#include "../impl/server-impls.cpp"
#include "mosquitto.h"
#include "include/devmem.hpp"
#include <pthread.h>


#define DEFAULT_SLEEP 125000 //microseconds
// the server with all implementations
#define mqtt_host "192.168.1.104"
//#define mqtt_host "localhost"
#define mqtt_port 1883

static int run = 1;
struct mosquitto *mosq;
pthread_t cmd_thread;
pthread_t points[4];

typedef struct
{
	int type;
	char mode;
	char *payload;
	int last;
} progress_info;

typedef struct{
	int signal;
	Client* client;
	Point* p;
	Trajectory* t;
	bool error;
} CommandObjectStruct;

progress_info progress;

bool executing_trajectory = false;

void parse_command(char *command, int *t, char *m, char *url, int *n,int* sleep);
void ftp_trajectory(char *url);

void* home_func(void* arg){
	CommandObjectStruct* output = (CommandObjectStruct*)arg;
	int signal = output->signal;
	Client* client = output->client;
	Point* p = output->p;
	Trajectory* t = output->t;
	printf("signal: %d\n",signal);
	printf("point: %s\n",p->to_json().dump().c_str());
	printf("trajectory: %s\n",t->to_json().dump().c_str());
	json client_js = client->to_json();
	std::string id = client_js["id"];
	std::string str_c = client_js.dump();
	const char* client_c = str_c.c_str();
	printf("client: %s\n",client_c);
	
	
	//system("/home/root/home");
	usleep(100);
	output->signal = ARM_HOME_SEARCHED;
	//json js = output->to_json();
	// std::string str = js.dump();
	// const char* c_str = str.c_str();
	// publish_message("EDScorbot/commands",c_str);

	std::cout << "Home position reached" << std::endl;
	return NULL;
}

void handle_signal(int s)
{
	run = 0;
}

void subscribe_all_topics()
{
    printf("Subscribing on topic metainfo\n");
    mosquitto_subscribe(mosq, NULL, "metainfo", 0);
    printf("Subscribing on topic EDScorbot/commands\n");
    mosquitto_subscribe(mosq, NULL, "EDScorbot/commands", 0);
}

int publish_message(const char *topic, const char *buf)
{
    char *payload = (char *)buf;
	int rc = mosquitto_publish(mosq, NULL, topic, strlen(payload), payload, 1, false);
	//int *p = &rc;
	return rc;
}

void parse_command(char *command, int *t, char *m, char *url, int *n,int *sleep)
{
	char *pch;

	pch = strtok(command, "[],");
	int type = atoi(pch);
	*t = type;
	pch = strtok(NULL, "[],");
	char mode = pch[0];
	*m = mode;
	pch = strtok(NULL, "[],");
	// char buf[100];
	strcpy(url, pch);
	pch = strtok(NULL, "[],");
	*n = atoi(pch);
	pch = strtok(NULL, "[],");
	*sleep = atoi(pch);
// url = buf;
#ifdef EDS_VERBOSE

	printf("type: %d\n", type);
	printf("mode: %c\n", mode);
	printf("url: %s\n", url);
	printf("n: %d\n", *n);

#endif
}

void handle_metainfo_message(std::string mesage){
	MetaInfoObject mi = initial_metainfoobj();
	publish_message("metainfo",mi.to_json().dump().c_str());
}

void handle_commands_message(const struct mosquitto_message *message){
	int sig = extract_signal((char *)message->payload);
	CommandObject output = CommandObject(ARM_STATUS);
				CommandObject receivedCommand = CommandObject::from_json_string((char *)message->payload);
				switch (sig){				
					case ARM_CHECK_STATUS:
						std::cout << "Request status received. " << " Sending message..." << std::endl;
						publish_message("EDScorbot/commands",output.to_json().dump().c_str());
						break;
					case ARM_CONNECT:
						std::cout << "Request comnnect received. " << " Sending message..." << std::endl;
						
						if(!owner.is_valid()){
							owner = receivedCommand.client;
							output.signal = ARM_CONNECTED;
							output.client = owner;
							publish_message("EDScorbot/commands",output.to_json().dump().c_str());
							std::cout << "Moving arm to home..." << std::endl;
							//Ejecucion del home
							CommandObjectStruct co;
							
							co.client = &receivedCommand.client;
							co.error = error_state;
							co.p = &receivedCommand.point;
							co.t = &receivedCommand.trajectory;
							co.signal = receivedCommand.signal;
							int err = pthread_create(&cmd_thread,NULL,&home_func,(void*)&co);
							pthread_detach(cmd_thread);
							

							
						} else{
							std::cout << "Connection refused. Arm is busy" << std::endl;
						}
						
						break;
					case ARM_MOVE_TO_POINT:
						std::cout << "Move to point request received. " << std::endl;
						
						if(owner.is_valid()){
							Client client = receivedCommand.client;
							if(owner == client){	
								Point target = receivedCommand.point;
								//if the point does not come within the message?
								//coger las 4 referencias
								int i;
							
							//	move_to_point_and_publish(target);
							} else {
								//other client is trying to move the arm ==> ignore
							}
						} else {
							//arm has no owner ==> ignore
						}
						break;
					case ARM_APPLY_TRAJECTORY:
						std::cout << "Apply trajectory received. " << std::endl;
						if(owner.is_valid()){
							Client client = receivedCommand.client;
							if(owner == client){	
								Trajectory traj = receivedCommand.trajectory;
								std::thread thread_trajectory(apply_trajectory_and_publish,traj);
								thread_trajectory.join();
							} else {
								//other client is trying to move the arm ==> ignore
							}
						} else {
							//arm has no owner ==> ignore
						}
						break;
					case ARM_CANCEL_TRAJECTORY:
						std::cout << "Cancel trajectory received. " << std::endl;
						if(owner.is_valid()){
							executing_trajectory = false;
							output.signal = ARM_CANCELED_TRAJECTORY;
							output.client = owner;
							output.error = error_state;
							publish_message("EDScorbot/commands",output.to_json().dump().c_str());
							std::cout << "Trajectory cancelled. " << std::endl;
						} else {
							//arm has no owner ==> ignore
						}
						break;
					case ARM_DISCONNECT:
						std::cout << "Request disconnect received. " << std::endl;
						Client c = receivedCommand.client;
						if(c == owner){
							owner = Client();
							output.signal = ARM_DISCONNECTED;
							output.client = c;
							publish_message("EDScorbot/commands",output.to_json().dump().c_str());
							std::cout << "Client disconnected" << std::endl;
						}
						
						break;
						//incluir default
					//default:
				}
}

//point is [j1,j2,j3,j4]
void* move_to_point_and_publish(void* arg) {
    
	Point* p = (Point*) arg;
	//std::cout << "Moving arm to point " << point.to_json().dump() << std::endl;
	sleep(1);
	//TODO
	// invoke command to move the arm to a specific position (point with degrees)
	// gets the values and build a real point 
	//system("/home/root/sendRef ")
	int i;
	int refs[4];

	// for(i = 0;i<4;i++){
	// 	int ref = angle_to_ref(i+1,point.coordinates[i]);
	// 	refs[i] = ref;
	// }



	usleep(DEFAULT_SLEEP);

	int* dev = open_devmem();
	MovedObject output = MovedObject();
	for (i = 0; i<6;i++){
		
		output.content.coordinates[i] = dev[i+1];
	}
	//Point realPoint = point; //change this assignment with the real point coordinates
	

	output.client = owner;
    output.error = error_state;
    //output.content = realPoint; //
    publish_message("EDScorbot/moved",output.to_json().dump().c_str());
	std::cout << "Point published " << output.to_json().dump().c_str() << std::endl;
}

void apply_trajectory_and_publish(Trajectory trajectory){
	std::list<Point> points = std::list<Point>(trajectory.points);
	executing_trajectory = true;
	while (!points.empty() && executing_trajectory){
        Point p = points.front();
		//move_to_point_and_publish(p);
		points.erase(points.begin());
	}
	executing_trajectory = false;
}

void message_callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message *message)
{

	//if the message contains a signal then it has came from a client (angular)
	//then follows the new communication model. otherwise, it does exactly as before
	bool new_flow = has_signal((char *) message->payload);
	if(new_flow){

		bool match = std::strcmp(message->topic,"metainfo") == 0;
		int sig = extract_signal((char *)message->payload);
		if(match){
			if(sig == ARM_GET_METAINFO){
				handle_metainfo_message((char *)message->payload);
			}

		} else {
			match = std::strcmp(message->topic,"EDScorbot/commands") == 0;
			if (match){
				handle_commands_message(message);
				
			}
		}

	} else {

		bool match = 0;

		mosquitto_topic_matches_sub("/EDScorbot/commands", message->topic, &match);
		if (match)
		{
#ifdef EDS_VERBOSE
			printf("got message for /EDScorbot/commands topic\n");
#endif

			int type, n, sleep;
			char mode;
			char url[100];
			parse_command((char *)message->payload, &type, &mode, url, &n,&sleep);
			progress.type = type;
			progress.mode = mode;
			progress.payload = url;
			progress.last = 1;
			char *cmd, *out_fname;
			
			switch (progress.type)
			{
			case 1:
				// Trajectory
				if (progress.mode == 'S')
				{
					cmd = reinterpret_cast<char *>(malloc(512));
					out_fname = reinterpret_cast<char *>(malloc(100));
					int l = strlen(progress.payload);
					
					
					for (int i = 0; i < l; i++)
					{
						out_fname[i] = progress.payload[i];
						if (l - i < 7)
						{
							char aux[15] = "_out_cont.json";
							strcat(out_fname,aux);
							break;
						}
					}

					snprintf(cmd, 512, "/home/root/trajectory -c /home/root/initial_config.json -n %d -p 100 -cont %s -s %d %s > log.txt &", n,out_fname,sleep*1000,progress.payload);
					printf("%s",cmd);
					system(cmd);
				}
				break;
			case 2:
				// Move joints
				cmd = reinterpret_cast<char *>(malloc(300));
				// Not really progress nor n, don't know how to solve this right now :P
				snprintf(cmd, 300, "/home/root/sendRef %d %d", progress.mode, n);
				system(cmd);
				break;
			case 3:
				// Reset spid (ConfigureInit)
				cmd = reinterpret_cast<char *>(malloc(20));
				snprintf(cmd, 20, "/home/root/reset");
				system(cmd);
				break;
			case 4:
				// Home
				cmd = reinterpret_cast<char *>(malloc(20));
				snprintf(cmd, 20, "/home/root/home");
				system(cmd);
				break;

			default:
				// free(cmd);
				break;
			}
			free(cmd);
		}
	}


}


// esto va en el archivo trajectory.cpp
void *publish(void *buf)
{
	char *payload = (char *)buf;
	int rc = mosquitto_publish(mosq, NULL, "/EDScorbot/trajectory", strlen(payload), payload, 1, false);
	int *p = &rc;
	void *v = (void *)p;
	return v;
}

void ftp_trajectory(char *url)
{

	// descargar trayectoria y ejecutarla
	// system("execute_trajectory ....");
	// pthread_t pub_thread;
}

int main(int argc, char *argv[])
{

	uint8_t reconnect = true;
	char clientid[24];
	int rc = 0;

	signal(SIGINT, handle_signal);
	signal(SIGTERM, handle_signal);

	mosquitto_lib_init();

	memset(clientid, 0, 24);
	snprintf(clientid, 23, "mqtt_server_%d", getpid());
	mosq = mosquitto_new(clientid, true, NULL);
	progress.last = 0;
	if (mosq)
	{
		mosquitto_message_callback_set(mosq, message_callback);
    
		rc = mosquitto_connect(mosq, mqtt_host, mqtt_port, 60);

        subscribe_all_topics();

		MetaInfoObject mi = initial_metainfoobj();
		publish_message("metainfo",mi.to_json().dump().c_str());
		std::cout << "Metainfo published " << mi.to_json().dump().c_str() << std::endl;
		
		rc = mosquitto_loop_start(mosq);
		while (run)
		{
			
			if (run && rc)
			{
				printf("connection error!\n");
				sleep(1);
				mosquitto_reconnect(mosq);
			}
            else
            {
                //printf("server conected to mosquitto broker!\n");
            }
		}
		mosquitto_loop_stop(mosq,true);
		mosquitto_destroy(mosq);
	}

	mosquitto_lib_cleanup();

	return rc;
}