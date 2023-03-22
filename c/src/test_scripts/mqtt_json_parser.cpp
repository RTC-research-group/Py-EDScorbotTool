
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <string>
#include <iostream> 
#include "mosquitto.h"
#include "nlohmann/json.hpp"




using json = nlohmann::json;

static int running = 1;
class JointInfo
{
public:
	double minimum;
	double maximum;

	JointInfo()
	{
	}

	JointInfo(double min, double max)
	{
		minimum = min;
		maximum = max;
	}
	void set_minimum(double min)
	{
		minimum = min;
	}

	void set_maximum(double max)
	{
		maximum = max;
	}
	std::string to_jsonstring(){
		
		// json js;
		// js["minimum"] = this->minimum;
		// js["maximum"] = this->maximum;
		// std::string s(js.dump().c_str());
		

		// return s;
	}
};
//controller name
const std::string CONTROLLER_NAME = "EDScorbot";

// metainfo constants
const int ARM_GET_METAINFO = 1;
const int ARM_METAINFO = 2;

// commands constants
const int ARM_CHECK_STATUS = 3;
const int ARM_STATUS = 4;
const int ARM_CONNECT = 5;
const int ARM_CONNECTED = 6;
const int ARM_MOVE_TO_POINT = 7;
const int ARM_APPLY_TRAJECTORY = 8;
const int ARM_CANCEL_TRAJECTORY = 9;
const int ARM_CANCELED_TRAJECTORY = 10;
const int ARM_DISCONNECT = 11;
const int ARM_DISCONNECTED = 12;
const int ARM_HOME_SEARCHED = 13;

// subtopics for each robot
const std::string META_INFO = "metainfo";
const std::string COMMANDS = "commands";
const std::string MOVED = "moved";

void parse_json_mqtt(char *command)
{

	json aux = json::parse(command);
	//aux.parse(command);
	std::cout << aux["error"] << std::endl;
	for (const auto &[k, v] : aux.items())
    {
        std::cout << "k: " << k << std::endl;
		std::cout << "v: " << v << std::endl;

        
        // std::cout << "Key: " << k << std::endl;
        // std::cout << "Value: " << v[1] << std::endl;
    }
	json joints = aux["joints"];
	for (const auto &[k, v] : joints.items()){
		std::cout << "\tk: " << k << std::endl;
		std::cout << "\tv: " << v << std::endl;
	} 

	running = 0;
}

void callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message *message){
	
bool match = 0;
	// printf("got message '%.*s' for topic '%s'\n", message->payloadlen, (char*) message->payload, message->topic);

	

	mosquitto_topic_matches_sub("metainfo", message->topic, &match);
	if (match)
	{
		parse_json_mqtt((char*)message->payload);
	}


} 




const JointInfo metainfo[] = 
{
    JointInfo(-450, 500),
    JointInfo(-950, 800),
    JointInfo(-350, 350),
    JointInfo(-1500, 1600),
    JointInfo(-360, 360),
    JointInfo(0, 100)
};


int main()
{
	int rc;
	struct mosquitto *mosq;
	
	mosquitto_lib_init();

	mosq = mosquitto_new("parser-test", true, NULL);

	rc = mosquitto_connect(mosq, "192.168.1.104", 1883, 60);
	if (rc != 0)
	{
		printf("Client could not connect to broker! Error Code: %d\n", rc);
		mosquitto_destroy(mosq);
		return -1;
	}
	printf("We are now connected to the broker!\n");
	mosquitto_message_callback_set(mosq,callback);
	mosquitto_subscribe(mosq,NULL,"metainfo",0);
	mosquitto_loop_start(mosq);
	while(running){
		sleep(1);
	} ; 
	mosquitto_loop_stop(mosq,false);
	
	// mosquitto_publish(mosq, NULL, "test/t1", 6, "Hello", 0, false);

	mosquitto_disconnect(mosq);
	mosquitto_destroy(mosq);

	mosquitto_lib_cleanup();
	return 0;
}
