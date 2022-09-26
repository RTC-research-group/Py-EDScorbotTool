#include "utils.h"
using json = nlohmann::json;


int main(int argc, char *argv[])
{
    // argv[1] --> datos en json
    
    std::vector<int> j1,j2,j3,j4,j5,j6;
    //float j1[500], j2[500];
    parse_jsonnp_array(argv[1], &j1[0], &j2[0],&j3[0],&j4[0],&j5[0],&j6[0]);
    // printf("%f,%f\n", j1[0], j2[0]);
    float j1_angles[500], j2_angles[500];
    std::vector<float> j1_angles,j2_angles,j3_angles,j4_angles,j5_angles,j6_angles;
    w_to_angles(j1_angles, j2_angles,j3_angles, j4_angles,j5_angles, j6_angles, j1, j2,j3, j4,j5, j6);

    // Inicializacion scorbot
    // argv[2] --> initial_config.json
    char *config_file = argv[2];
    EDScorbot handler(config_file);

    //Arbitrary size vectors, for collecting data while we wait for the robot to reach a position
    std::vector<int> j1_vector, j2_vector;
    //
    std::vector<timeval> timestamp_vector;
    std::vector<robot_state> state_vector;



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

        long int elapsed = time_in_micros(end) - time_in_micros(start);
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
            elapsed = time_in_micros(end) - time_in_micros(start);
        }

        snprintf(mqtt_msg, MAX_MQTT_MSG, "[%d,%d,%d,%d,%d,%d,%d]", joints[0], joints[1], joints[2], joints[3], joints[4], joints[5], i);
        publish(mosq, mqtt_msg, strlen(mqtt_msg), "EDScorbot/trajectory");
        j1_pos[i] = j1_vector.back();
        j2_pos[i] = j2_vector.back();
        timestamp_arr[i]=timestamp_vector.back();
    }

    
    write_array("./j1_counters_output");
    
    
    FILE *fj1 = fopen("./j1_counters_output", "wb");
    int *pv = &j1_vector[0];
    fwrite((const void *)pv, 4, j1_vector.size(), fj1);
    fclose(fj1);

    FILE *fj2 = fopen("./j2_counters_output", "wb");
    pv = &j2_vector[0];
    fwrite((const void *)pv, 4, j2_vector.size(), fj2);
    fclose(fj2);

    FILE *ts = fopen("./timestamp_output", "wb");
    struct timeval* pts = &timestamp_vector[0];
    fwrite((const void *)pts, 8, timestamp_vector.size(), ts);
    fclose(ts);

    FILE *fj1_500 = fopen("./j1_counters_output_500", "wb");
    pv = &j1_pos[0];
    fwrite((const void *)pv, 4,500, fj1_500);
    fclose(fj1_500);

    // Ejecucion de la trayectoria con j1 y j2

    // Recogida de resultados? Listas de c++ o arrays de c?

    // Conversion y envío de resultados en json
    publish(mosq, "[-1,-1,-1,-1,-1,-1,-1]", strlen("[-1,-1,-1,-1,-1,-1,-1]"), "EDScorbot/trajectory");

    return 0;
}


