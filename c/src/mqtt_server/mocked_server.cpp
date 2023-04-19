#include <signal.h>
#include <iostream>
#include <string>
#include <thread>
#include <unistd.h>
#include "../impl/server-impls.cpp"
#include "mosquitto.h"
#include "include/devmem.hpp"
#include <pthread.h>
#include "include/EDScorbot.hpp"
#include <vector>

#define DEFAULT_SLEEP 125000 //microseconds
// the server with all implementations
#define mqtt_host "192.168.1.104"
//#define mqtt_host "localhost"
#define mqtt_port 1883

static int run = 1;
struct mosquitto *mosq;
pthread_t search_home_thread;
pthread_t move_to_point_thread;
pthread_t apply_trajectory_thread;

typedef struct
{
	int type;
	char mode;
	char *payload;
	int last;
} progress_info;

typedef struct{
	Point p;
	std::string config;
	int sleep;
} pthread_args,*ppthread_args;

progress_info progress;
static ppthread_args args;

Point current_point;

bool executing_trajectory = false;

void parse_command(char *command, int *t, char *m, char *url, int *n,int* sleep);
void ftp_trajectory(char *url);

// void update_pthread_args(ppthread_args args,std::string& config, int sleep, Point& p){
	
// 	args.config = config;
// 	args.p = p;
// 	args.sleep = sleep;

// }

void* search_home_threaded_function(void* arg){
	//to execute search home we need the suitable signal, the owner and the error state
	// the owrner has already been validated to allow this execution in the callback
	CommandObject output = CommandObject(ARM_HOME_SEARCHED);
	char* config = (char*)arg;
	output.client = owner;
	output.error = error_state; 

	//usleep(4000000);
	EDScorbot handler("/home/root/initial_config.json");
	handler.searchHome(handler.j2,false);
	handler.searchHome(handler.j3,false);
	handler.searchHome(handler.j1,false);
	//system("/home/root/home");
	
	//publish message notifying that home has been reached
	publish_message("EDScorbot/commands",output.to_json().dump().c_str());
	std::cout << "Home position reached" << std::endl;
	return NULL;
}

//Arguments
//Point (j1,j2,j3,j4)
//config char*

void* move_to_point_threaded_function(void* arg){
	//to move to a single point we need the owner, the error state and the point
	// the owrner has already been validated to allow this execution in the callback
	ppthread_args args = reinterpret_cast<ppthread_args>(arg);
	std::string config = args->config;
	// Point *p;
	// p = &(args->p);
	MovedObject output = MovedObject();
	output.client = owner;
	output.error = error_state;
	
	EDScorbot handler("/home/root/initial_config.json");	//call the low level function to move to a single point considering 
	
	std::vector<double> coords = current_point.coordinates;
	int i;
	for(i = 0; i < 4 ; i++){
		int ref = angle_to_ref(i+1,coords[i]);
		handler.sendRef(ref,handler.joints[i]);
	}
	
		delete &handler;

	//the coordinates (in refs) stored in current_point (current_point.coordinates) 
	//system("/home/root/home");

	//get the counters from the arm and convert them into refs to return to the user
	//it is important to fill the coordinates with the number of joints
	//informed in the metainfo. 

	//using this snipped of code to fill the real point
	usleep(DEFAULT_SLEEP);
	//usleep(2000000);

	//int* dev = open_devmem();
	//for (int i = 0; i < 6; i++){
	//	output.content.coordinates[i] = dev[i+1];
	//}

	//for the moment we use current_point to notify the user
	double angles[6];
	handler.readJoints(angles);
	Point reached;
	std::vector<double> reached_v;

	
	for(i = 0; i< 6;i++){
		reached_v.push_back(angles[i]);
	}

	reached.coordinates = reached_v;
	output.content = reached;
	
	//publish message notifying that the point has been published
	publish_message("EDScorbot/moved",output.to_json().dump().c_str());
	std::cout << "Arm moved to point " << output.content.to_json().dump().c_str() << std::endl;

	//after publishing the message, the current_point must be re-instantiated with empty point
	current_point = Point();

	return NULL;
}



//the function below is intented to be used in trajectory execution because the execution of 
//alll points of a trajectory cannot be threaded (different points would be execut4ed concurrently,
//causing a terrible side-effect)
void move_to_point(Point point,ppthread_args args){
	MovedObject output = MovedObject();
	output.client = owner;
	output.error = error_state; 
	
	
	//call the low level function to move to a single point considering 
	//the coordinates (in refs) stored in oint (point.coordinates) 
	//system("/home/root/home");
	//update_pthread_args(args,args->config,args->sleep,point);
	pthread_create(&move_to_point_thread,NULL,move_to_point_threaded_function,reinterpret_cast<void*>(args));
	//get the counters from the arm and convert them into refs to return to the user
	//it is important to fill the coordinates with the number of joints
	//informed in the metainfo. 

	//using this snipped of code to fill the real point
	//usleep(DEFAULT_SLEEP);
	//usleep(2000000);

	//int* dev = open_devmem();
	//for (int i = 0; i < 6; i++){
	//	output.content.coordinates[i] = dev[i+1];
	//}

	//for the moment we use point to notify the user
	output.content = point;

	//publish message notifying that the point has been published
	publish_message("EDScorbot/moved",output.to_json().dump().c_str());
	std::cout << "Arm moved to point " << output.content.to_json().dump().c_str() << std::endl;
	return;
}

Trajectory current_trajectory;

void* apply_trajectory_threaded_function(void* arg){
	//to apply a trajectory we need the owner, the error state and the trajectory
	// the owner has already been validated to allow this execution in the callback
	//the current trajectory is maintained in a global variable current_trajectory
	//that is updated befoe starting this thread

	MovedObject output = MovedObject();
	output.client = owner;
	output.error = error_state; 

	ppthread_args traj_args = reinterpret_cast<ppthread_args>(arg);
	std::string config = traj_args->config;
	int sleep = traj_args->sleep;
	std::list<Point> points = std::list<Point>(current_trajectory.points);
	executing_trajectory = true;
	EDScorbot handler("/home/root/initial_config.json");
	int i;
	int ref;
	while (!points.empty() && executing_trajectory){
		
        Point p = points.front();

		//move_to_point(p,); 
		
		for(i = 0; i< 4;i++){
			ref = angle_to_ref(i+1,p.coordinates[i]);
			handler.sendRef(ref,handler.joints[i]);
		}
		double angles[6];
		handler.readJoints_angle(angles);
		Point reached;

		std::vector<double> reached_v;

	
		for(i = 0; i< 6;i++){
			reached_v.push_back(angles[i]);
		}
		
		output.content = reached;
		//publish message notifying that the point has been published
		publish_message("EDScorbot/moved",output.to_json().dump().c_str());
		std::cout << "Arm moved to point " << output.content.to_json().dump().c_str() << std::endl;
		int s =  (int) (p.coordinates.back());
		usleep(s);
		
		//we need to handle the waiting time after start oving to a point.
		//this time is the last coordinate of the point parameter
		//usleep(p.coordinates.end()) // something like this ??????

		points.erase(points.begin());

	}

	executing_trajectory = false;
	current_trajectory = Trajectory();
	

	// there is no need to publish when the trajectory is finished 
	// because the graphical interface waits for a message in moved 
	// that is not returned and it itnerprets as the trajectory has been finished successfully
	//Publish somehting no?
	//publish_message("EDScorbot/commands","TRAJECTORY_COMPLETED"); //o algo asi
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
							//output.point.coordinates = std::vector<double>();

							publish_message("EDScorbot/commands",output.to_json().dump().c_str());
							std::cout << "Moving arm to home..." << std::endl;
							
							int err = pthread_create(&search_home_thread,NULL,&search_home_threaded_function,NULL);
							pthread_detach(search_home_thread);

							//handle err?

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
								if(!target.is_empty()){
									current_point = target;
									//update_pthread_args(args,args->config,args->sleep,target);
									int err = pthread_create(&move_to_point_thread,NULL,&move_to_point_threaded_function,args);
									pthread_detach(move_to_point_thread);

									//handle err?
								}
							} else {
								printf("err1");
								//other client is trying to move the arm ==> ignore
							}
						} else {
							printf("err2");
							//arm has no owner ==> ignore
						}
						break;
					case ARM_APPLY_TRAJECTORY:
						std::cout << "Apply trajectory received. " << std::endl;
						if(owner.is_valid()){
							Client client = receivedCommand.client;
							if(owner == client){	
								current_trajectory = receivedCommand.trajectory;
								//update_pthread_args(args,args->config,args->sleep,args->p);
								int err = pthread_create(&apply_trajectory_thread,NULL,&apply_trajectory_threaded_function,args);
								pthread_detach(apply_trajectory_thread);

								//handle err?
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
							Client client = receivedCommand.client;
							if(owner == client){
								executing_trajectory = false;
								output.signal = ARM_CANCELED_TRAJECTORY;
								output.client = owner;
								output.error = error_state;
								publish_message("EDScorbot/commands",output.to_json().dump().c_str());
								std::cout << "Trajectory cancelled. " << std::endl;
							} 
							
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
 	argparse::ArgumentParser parser("mocked_server");
    parser.add_argument("-c", "--config_file").help("Optional. Configuration file in JSON format. This file can be used to configure each joint's controller parameters. Default is 'initial_config.json'").default_value(std::string("/home/root/initial_config.json"));
    parser.add_argument("-v", "--verbose").help("Increase verbosity of output").default_value(false).implicit_value(true);

    try
    {
        parser.parse_args(argc, argv);
    }
    catch (const std::runtime_error &err)
    {
        std::cerr << err.what() << std::endl;
        std::cerr << parser;
        std::exit(1);
    }

    std::string config_file = parser.get<std::string>("--config_file");
    bool verbose = parser.get<bool>("--verbose");
	Point p;
    //update_pthread_args(*args,config_file,DEFAULT_SLEEP,p);
    
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