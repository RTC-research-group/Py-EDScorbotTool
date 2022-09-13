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
using json = nlohmann::json;
#define SLEEP 250000
#define MAX_MQTT_MSG 200

// Function to parse numpy array in json format
void parse_jsonnp_array(char *filename, float *j1, float *j2);

// Function to transform a trajectory from angular velocities (w, omega) to angles
void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2);

void init_mqtt_client(mosquitto *mosq, char *broker_ip);
int publish(mosquitto *mosq, char *msg, int msg_len, char *topic);
void end_mqtt_client(mosquitto *mosq);
/*
int main()
{
    struct timeval stop, start;
    gettimeofday(&start, NULL);
    // do stuff
    gettimeofday(&stop, NULL);
    //printf("took %lu us\n", (stop.tv_sec - start.tv_sec) * 1000000 + stop.tv_usec - start.tv_usec);
    int i;
    for (i = 0; i < 1000; i++)
    {
        printf("i: %d, start: %li, end: %li, elapsed: %li\n", i, start.tv_usec, stop.tv_usec, stop.tv_usec - start.tv_usec);
        gettimeofday(&stop,NULL);
        //usleep(1000);
    }
}
*/

int main(int argc, char *argv[])
{
    // argv[1] --> datos en json

    float j1[500], j2[500];
    parse_jsonnp_array(argv[1], j1, j2);
    // printf("%f,%f\n", j1[0], j2[0]);
    float j1_angles[500], j2_angles[500];
    w_to_angles(j1_angles, j2_angles, j1, j2);

    // Inicializacion scorbot
    // argv[2] --> initial_config.json
    char *config_file = argv[2];
    EDScorbot handler(config_file);

    //Arbitrary size vectors, for collecting data while we wait for the robot to reach a position
    std::vector<int> j1_vector, j2_vector;
    //
    std::vector<timeval> timestamp_vector;
    //500 point arrays, to send data back to the l2l model
    int j1_pos[500], j2_pos[500];
    struct timeval timestamp_arr[500];

    handler.initJoints();

    mosquitto_lib_init();

    struct mosquitto *mosq;
    mosq = mosquitto_new(NULL, true, 0);

    init_mqtt_client(mosq, "192.168.1.104");
    char mqtt_msg[MAX_MQTT_MSG];

    int i;
    for (i = 0; i < 500; i++)
    {
        int refj1, refj2;
        refj1 = handler.angle_to_ref(1, j1_angles[i]);
        refj2 = handler.angle_to_ref(2, j2_angles[i]);
        printf("It: %d, J1: %d, J2: %d\n", i, refj1, refj2);
        handler.sendRef(refj1, handler.j1);
        handler.sendRef(refj2, handler.j2);
        struct timeval start, end;
        gettimeofday(&start, NULL);
        gettimeofday(&end, NULL);

        // clock_t start = clock();
        // clock_t end = clock();
        int joints[6];

        long int elapsed = ((end.tv_sec - start.tv_sec) * 1000000) + end.tv_usec - start.tv_usec;
        while (elapsed < SLEEP)
        {
            // Do something
            // printf("start: %li, stop:%li, elapsed: %li\n",start.tv_usec,end.tv_usec,elapsed);
            handler.readJoints(joints);
            j1_vector.push_back(joints[0]);
            j2_vector.push_back(joints[1]);
            timestamp_vector.push_back(end);
            (gettimeofday(&end, NULL));
            // while (!ret){
            //     ret = (gettimeofday(&end, NULL));
            // }
            elapsed = ((end.tv_sec - start.tv_sec) * 1000000) + end.tv_usec - start.tv_usec;
        }

        snprintf(mqtt_msg, MAX_MQTT_MSG, "[%d,%d,%d,%d,%d,%d,%d]", joints[0], joints[1], joints[2], joints[3], joints[4], joints[5], i);
        publish(mosq, mqtt_msg, strlen(mqtt_msg), "EDScorbot/trajectory");
        j1_pos[i] = j1_vector.back();
        j2_pos[i] = j2_vector.back();
        timestamp_arr[i]=timestamp_vector.back();
    }

    FILE *fj1 = fopen("./j1_counters_output", "wb");
    int *pv = &j1_vector[0];
    fwrite((const void *)pv, 4, j1_vector.size(), fj1);
    fclose(fj1);

    FILE *fj2 = fopen("./j2_counters_output", "wb");
    pv = &j2_vector[0];
    fwrite((const void *)pv, 4, j2_vector.size(), fj2);
    fclose(fj2);

    FILE *ts = fopen("./timestamp_output", "wb");
    pv = &timestamp_vector[0];
    fwrite((const void *)pv, 4, timestamp_vector.size(), ts);
    fclose(ts);

    // Ejecucion de la trayectoria con j1 y j2

    // Recogida de resultados? Listas de c++ o arrays de c?

    // Conversion y envío de resultados en json
    publish(mosq, "[-1,-1,-1,-1,-1,-1,-1]", strlen("[-1,-1,-1,-1,-1,-1,-1]"), "EDScorbot/trajectory");

    return 0;
}

void parse_jsonnp_array(char *filename, float *j1, float *j2)
{
    std::ifstream arr_stream(filename, std::ios::in);
    json array = json::parse(arr_stream);

    for (const auto &[k, v] : array.items())
    {
        int i = atoi(k.c_str());
        j1[i] = v[0];
        j2[i] = v[1];
        // std::cout << "Key: " << k << std::endl;
        // std::cout << "Value: " << v[1] << std::endl;
    }
    return;
}

void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2)
{
    j1_angles[0] = (j1[0] * 0.001) * (180 / PI);
    j2_angles[0] = (j2[0] * 0.001) * (180 / PI);
    int i = 0;
#ifdef DEBUG
    printf("[%f\t%f ]\n", j1_angles[i], j2_angles[i]);
#endif

    for (i = 1; i < 500; i++)
    {
        // np.cumsum(omegas * 0.001,axis=0)*( 180 / np.pi)
        j1_angles[i] = (j1[i] * (0.001) * (180 / PI)) + j1_angles[i - 1];
        j2_angles[i] = (j2[i] * (0.001) * (180 / PI)) + j2_angles[i - 1];
#ifdef DEBUG
        printf("[%f\t%f ]\n", j1_angles[i], j2_angles[i]);
#endif
    }
}

void init_mqtt_client(mosquitto *mosq, char *broker_ip)
{
    int rc;
    
    rc = mosquitto_connect(mosq, broker_ip, 1883, 60);
    while (rc != 0)
    {
        printf("Client could not connect to broker! Error Code: %d\nTrying to reconnect...\n", rc);
        rc = mosquitto_connect(mosq, broker_ip, 1883, 60);

        // mosquitto_destroy(mosq);
        // return -1;
    }
    printf("We are now connected to the broker!\n");

    // SUBSCRIBE!
}

int publish(mosquitto *mosq, char *msg, int msg_len, char *topic)
{
    int ret = mosquitto_publish(mosq, NULL, topic, msg_len, topic, 0, false);
    return ret;
}

void end_mqtt_client(mosquitto *mosq)
{
    mosquitto_disconnect(mosq);
    mosquitto_destroy(mosq);

    mosquitto_lib_cleanup();
}


