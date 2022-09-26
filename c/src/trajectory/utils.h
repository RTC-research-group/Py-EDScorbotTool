#include "nlohmann/json.hpp"

#include <map>
#include <iostream>
#include <fstream>
#include <vector>
#include <unistd.h>
#include <sys/time.h>
#include "mosquitto.h"
#include "include/EDScorbot.hpp"
#define PI 3.141592653589793
#define SLEEP 250000
#define MAX_MQTT_MSG 200


/**
 * @brief Struct to hold robot state, including timestamp
 * 
 * 
 * 
 */
typedef struct{

    int j1;
    int j2;
    int j3;
    int j4;
    int j5;
    int j6;
    int timestamp;
}
robot_state;


/// Function to parse numpy array in json format
void parse_jsonnp_array(char *filename, float *j1, float *j2);

/// Function to transform a trajectory from angular velocities (w, omega) to angles
void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2);

void init_mqtt_client(mosquitto *mosq, char *broker_ip);
int publish(mosquitto *mosq, char *msg, int msg_len, char *topic);
void end_mqtt_client(mosquitto *mosq);

long int time_in_micros(timeval t);
void write_array(char* fname, const void* data,int size,int n);