#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "mosquitto.h"
#include "nlohmann/json.hpp"
using json = nlohmann::json;


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
		
		json js;
		js["minimum"] = this->minimum;
		js["maximum"] = this->maximum;
		std::string s(js.dump().c_str());
		

		return s;
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

	mosq = mosquitto_new("publisher-test", true, NULL);

	rc = mosquitto_connect(mosq, "192.168.1.104", 1883, 60);
	if (rc != 0)
	{
		printf("Client could not connect to broker! Error Code: %d\n", rc);
		mosquitto_destroy(mosq);
		return -1;
	}
	printf("We are now connected to the broker!\n");
	{
		json js,joints;
		JointInfo metainfo[] =
			{
				JointInfo(-450, 500),
				JointInfo(-950, 800),
				JointInfo(-350, 350),
				JointInfo(-1500, 1600),
				JointInfo(-360, 360),
				JointInfo(0, 100)
				};
		js["signal"] = ARM_METAINFO;
		js["error"] = false;
		int i;
		for(i = 0; i < 6; i++){
			joints[i] = metainfo[i].to_jsonstring();
		}

		
		js["joints"] = joints;//Hace falta to_jsonstring
				

		mosquitto_publish(mosq, NULL, "metainfo", strlen(js.dump().c_str()), js.dump().c_str(), 0, false);
	}
	
	// mosquitto_publish(mosq, NULL, "test/t1", 6, "Hello", 0, false);

	mosquitto_disconnect(mosq);
	mosquitto_destroy(mosq);

	mosquitto_lib_cleanup();
	return 0;
}
