#include "utils.h"
#include <argparse/argparse.hpp>
using json = nlohmann::json;

int main(int argc, char *argv[])
{

    ///
    /// Argument parsing
    ///
    ///
    argparse::ArgumentParser parser("trajectory");
    parser.add_argument("trajectory_file").help("File which contains the trajectory in JSON format");
    parser.add_argument("n_points").help("Number of points of the trajectory. Integer").scan<'i', int>();
    parser.add_argument("-cont", "--out_cont").help("Optional. Base name of output files for counter values").default_value(std::string("out_cont"));
    parser.add_argument("-xyz", "--out_xyz").help("Optional. Base name of output files for xyz values").default_value(std::string("out_xyz"));
    parser.add_argument("-i", "--ip").help("Optional. IP of the MQTT broker to connect to. Default is ...").default_value(std::string("192.168.1.104"));
    parser.add_argument("-c", "--config_file").help("Optional. Configuration file in JSON format. This file can be used to configure each joint's controller parameters. Default is 'initial_config.json'").default_value(std::string("initial_config.json"));
    parser.add_argument("-s", "--sleep").help("Optional. Amount of microseconds to wait between joint commands. Default is 250000").default_value(int(250000));

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

    int n = parser.get<int>("n_points");
    const char *jsonnp_array_fname = parser.get<std::string>("trajectory_file").c_str();
    const char *ip = parser.get<std::string>("--ip").c_str();
    const char *config_file = parser.get<std::string>("--config_file").c_str();
    int SLEEP = parser.get<int>("--sleep");
    std::string out_cont = parser.get<std::string>("--out_cont");
    /// Load trajectory from file

    int *pjx[6];
    for (int i = 0; i < 6; i++)
    {
        pjx[i] = reinterpret_cast<int *>(malloc(sizeof(int) * n));
    }

    // float j1[500], j2[500];
    // parse_jsonnp_array(argv[1], &j1[0], &j2[0], &j3[0], &j4[0], &j5[0], &j6[0]);
    parse_jsonnp_array(jsonnp_array_fname, pjx[0], pjx[1], pjx[2], pjx[3], pjx[4], pjx[5]);
    // printf("%f,%f\n", j1[0], j2[0]);
    // float j1_angles[500], j2_angles[500];
    // std::vector<float> j1_angles,j2_angles,j3_angles,j4_angles,j5_angles,j6_angles;
    // w_to_angles(j1_angles, j2_angles,j3_angles, j4_angles,j5_angles, j6_angles, j1, j2,j3, j4,j5, j6);

    // Inicializacion scorbot
    // argv[2] --> initial_config.json

    EDScorbot handler(config_file);

    // Arbitrary size vectors, for collecting data while we wait for the robot to reach a position
    //  std::vector<int> j1_vector, j2_vector;
    //
    //  std::vector<timeval> timestamp_vector;
    std::vector<robot_state> state_vector;

    // 500 point arrays, to send data back to the l2l model
    int j1_pos[500], j2_pos[500];
    struct timeval timestamp_arr[500];

    handler.initJoints();

    mosquitto_lib_init();

    struct mosquitto *mosq;
    mosq = mosquitto_new(NULL, true, 0);

    init_mqtt_client(mosq, ip);
    char mqtt_msg[MAX_MQTT_MSG];

    for (int i = 0; i < n; i++)
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
            (gettimeofday(&end, NULL));
            robot_state rs;
            rs.j1 = joints[0];
            rs.j2 = joints[1];
            rs.j3 = joints[2];
            rs.j4 = joints[3];
            rs.j5 = joints[4];
            rs.j6 = joints[5];
            rs.timestamp = time_in_micros(end);
            state_vector.push_back(rs);

            // j1_vector.push_back(joints[0]);
            // j2_vector.push_back(joints[1]);
            // timestamp_vector.push_back(end);

            // while (!ret){
            //     ret = (gettimeofday(&end, NULL));
            // }
            elapsed = time_in_micros(end) - time_in_micros(start);
        }

        snprintf(mqtt_msg, MAX_MQTT_MSG, "[%d,%d,%d,%d,%d,%d,%d,%d]", joints[0], joints[1], joints[2], joints[3], joints[4], joints[5], time_in_micros(end), i);
        publish(mosq, mqtt_msg, strlen(mqtt_msg), "EDScorbot/trajectory");
        // j1_pos[i] = j1_vector.back();
        // j2_pos[i] = j2_vector.back();
        // timestamp_arr[i] = timestamp_vector.back();
    }
    publish(mosq, "[-1,-1,-1,-1,-1,-1,-1,-1]", strlen("[-1,-1,-1,-1,-1,-1,-1,-1]"), "EDScorbot/trajectory");
    json js;
    for (int i = 0; i < state_vector.size(); i++)
    {
        // Construir el json aqui
        js[i] = {state_vector[i].j1, state_vector[i].j2, state_vector[i].j3, state_vector[i].j4, state_vector[i].j5, state_vector[i].j6, state_vector[i].timestamp};
    }
    std::ofstream o(out_cont);
    o << std::setw(4) << js << std::endl; // Conversion y envío de resultados en json

    return 0;
}