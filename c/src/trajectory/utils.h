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


/**
 * @brief  Parse numpy array in json format
 * 
 * @param filename Name of the Numpy array in json format
 * @param jX Arrays of floats to hold values from Numpy array  
 */
void parse_jsonnp_array(char *filename, float *j1, float *j2,float *j3, float *j4,float *j5, float *j6);

/**
 * @brief  Transform a trajectory from angular velocities (w, omega) to angles
 * HAY QUE EXTENDERLA A 6 JOINTS
 * 
 * @param j1_angles 
 * @param j2_angles 
 * @param j1 
 * @param j2 
 */
void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2);

/**
 * @brief Initialise the mqtt client that will post progress updates to topic `/EDScorbot/trajectory`
 * 
 * @param mosq Pointer to `mosquitto` type (from mosquitto.h) object
 * @param broker_ip IP of the broker the client will connect to
 */

void init_mqtt_client(mosquitto *mosq, char *broker_ip);

/**
 * @brief Publish a message of arbitrary length (up to `MAX_MQTT_MSG`) to an arbitrary topic
 * 
 * @param mosq Pointer to `mosquitto` type (from mosquitto.h) object which has been previously initialised
 * @param msg Message to publish in the topic
 * @param msg_len Length of the message in bytes
 * @param topic Topic to publish to
 * @return int 
 */
int publish(mosquitto *mosq, char *msg, int msg_len, char *topic);

/**
 * @brief End mqtt session
 * 
 * @param mosq Pointer to `mosquitto` type (from mosquitto.h) object which has been previously initialised
 */
void end_mqtt_client(mosquitto *mosq);

/**
 * @brief Convert from `struct timeval` (time.h) to time in microseconds
 * 
 * This function takes a `timeval struct`, `t`, and sums its members `tv_sec` and `tv_usec` together and properly scaled to return the current time with
 * microsecond resolution
 * 
 * @param t `timeval struct` to convert to current time in microseconds
 * @return long int Time in microseconds
 */
long int time_in_micros(timeval t);

/**
 * @brief Read an array which was previously written to a file in binary format
 * 
 * @param v Array that will hold the data read from the file. Must be able to contain at least `size` elements of type `int`. This function will NOT check the array's size beforehand.
 * @param n Number of elements of size `sizeof(int)` to be read from file
 * @param filename Name of the file to be read
 * @return int 
 */
int read_array_from_file(int* v, int n, std::string filename);
/**
 * @brief Write the underlying int array from a vector to a file in binary format
 * 
 * @param v Vector that holds the data to be written (`&v[0]` is a pointer to the underlying array)
 * @param filename Name of the file to be written
 */
void write_vector_to_file(std::vector<int> v, std::string filename);
