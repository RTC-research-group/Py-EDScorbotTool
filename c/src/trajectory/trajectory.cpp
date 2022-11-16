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
    parser.add_argument("-n", "--n_traj").help("Index for a file with multiple trajectories. Check the format at URL").default_value(int(0)).scan<'i', int>();
    parser.add_argument("-cont", "--out_cont").help("Optional. Base name of output files for counter values").default_value(std::string("out_cont"));
    parser.add_argument("-xyz", "--out_xyz").help("Optional. Base name of output files for xyz values").default_value(std::string("out_xyz"));
    parser.add_argument("-i", "--ip").help("Optional. IP of the MQTT broker to connect to. Default is ...").default_value(std::string("192.168.1.104"));
    parser.add_argument("-c", "--config_file").help("Optional. Configuration file in JSON format. This file can be used to configure each joint's controller parameters. Default is 'initial_config.json'").default_value(std::string("initial_config.json"));
    parser.add_argument("-s", "--sleep").help("Optional. Amount of microseconds to wait between joint commands. Default is 250000").default_value(int(250000)).scan<'i', int>();
    parser.add_argument("-v", "--verbose").help("Increase verbosity of output").default_value(false).implicit_value(true);
    parser.add_argument("-p", "--percentage").help("Number of robot state samples that will be skipped after taking one. For a number of 100, 1 out of 100 observed positions will be recorded. Default is 100").default_value(int(100)).scan<'i', int>();

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

    int n = parser.get<int>("--n_traj");
    const char *jsonnp_array_fname = parser.get<std::string>("trajectory_file").c_str();
    const char *ip = parser.get<std::string>("--ip").c_str();
    const char *config_file = parser.get<std::string>("--config_file").c_str();
    int SLEEP = parser.get<int>("--sleep");
    bool verbose = parser.get<bool>("--verbose");
    std::string out_cont = parser.get<std::string>("--out_cont");
    int perc_mod = parser.get<int>("--percentage");
    /// Load trajectory from file

    /***/
    /***TO BE CHANGED*/
    std::ifstream arr_stream(jsonnp_array_fname, std::ios::in);
    json js = json::parse(arr_stream);


    int initial_position[6]={js["Joint_initial_positions"]["J1"],js["Joint_initial_positions"]["J2"],js["Joint_initial_positions"]["J3"],js["Joint_initial_positions"]["J4"],js["Joint_initial_positions"]["J5"],js["Joint_initial_positions"]["J6"]};
    assert(n>=0);
    char traj_index[5];
    snprintf(traj_index,5,"#%d",n);
    json trajectory = js["Trajectories"][traj_index];
    int n_steps = trajectory["steps"];

    // int *pjx[6];
    // for (int i = 0; i < 6; i++)
    // {
    //     pjx[i] = reinterpret_cast<int *>(malloc(sizeof(int) * n_steps));
    // }
    auto tj1 = trajectory["J1"];
    auto tj2 = trajectory["J2"];
    auto tj3 = trajectory["J3"];
    auto tj4 = trajectory["J4"];
    auto tj5 = trajectory["J5"];
    auto tj6 = trajectory["J6"];

    // float j1[500], j2[500];
    // parse_jsonnp_array(argv[1], &j1[0], &j2[0], &j3[0], &j4[0], &j5[0], &j6[0]);
    //parse_jsonnp_array(jsonnp_array_fname, pjx[0], pjx[1], pjx[2], pjx[3], pjx[4], pjx[5]);
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
    // int j1_pos[500], j2_pos[500];
    // struct timeval timestamp_arr[500];

    // handler.initJoints();
     handler.sendRef(initial_position[0],handler.j1);
     handler.sendRef(initial_position[1],handler.j2);
     handler.sendRef(initial_position[2],handler.j3);
     handler.sendRef(initial_position[3],handler.j4);
    mosquitto_lib_init();
    usleep(5000000); // Wait for 5 seconds to let the arm come back to home position
    struct mosquitto *mosq;
    mosq = mosquitto_new(NULL, true, 0);

    init_mqtt_client(mosq, ip);
    char mqtt_msg[MAX_MQTT_MSG];

    for (int i = 0; i < n; i++)
    {
        int refj1, refj2, refj3, refj4;
        //TO BE TESTED
        refj1 = tj1[i];
        refj2 = tj2[i];
        refj3 = tj3[i];
        refj4 = tj4[i];
        // refj1 = handler.angle_to_ref(1, j1_angles[i]);
        // refj2 = handler.angle_to_ref(2, j2_angles[i]);
        if (verbose)
        {
            printf("It: %d, J1: %d, J2: %d, J3: %d, J4: %d\n", i, refj1, refj2, refj3, refj4);
        }

        handler.sendRef(refj1, handler.j1);
        handler.sendRef(refj2, handler.j2);
        handler.sendRef(refj3, handler.j3);
        handler.sendRef(refj4, handler.j4);
        //  handler.sendRef(refj1, handler.j1);
        // handler.sendRef(refj2, handler.j2);
        struct timeval start, end;
        gettimeofday(&start, NULL);
        gettimeofday(&end, NULL);

        // clock_t start = clock();
        // clock_t end = clock();
        int joints[6];
        int j = 0;
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
            if (j % perc_mod == 0)
                state_vector.push_back(rs);

            // j1_vector.push_back(joints[0]);
            // j2_vector.push_back(joints[1]);
            // timestamp_vector.push_back(end);

            // while (!ret){
            //     ret = (gettimeofday(&end, NULL));
            // }
            elapsed = time_in_micros(end) - time_in_micros(start);
            j++;
        }

        snprintf(mqtt_msg, MAX_MQTT_MSG, "[%d,%d,%d,%d,%d,%d,%ld,%d]", joints[0], joints[1], joints[2], joints[3], joints[4], joints[5], time_in_micros(end), i);
        publish(mosq, mqtt_msg, strlen(mqtt_msg), std::string("EDScorbot/trajectory").c_str());
        // j1_pos[i] = j1_vector.back();
        // j2_pos[i] = j2_vector.back();
        // timestamp_arr[i] = timestamp_vector.back();
    }
    publish(mosq, "[-1,-1,-1,-1,-1,-1,-1,-1]", strlen("[-1,-1,-1,-1,-1,-1,-1,-1]"), std::string("EDScorbot/trajectory").c_str());
    json js1,js2,js3,js4,js5,js6,jstimestamp;
    for (int i = 0; i < state_vector.size(); i++)
    {
        // Construir el json aqui
        //js[i] = {state_vector[i].j1, state_vector[i].j2, state_vector[i].j3, state_vector[i].j4, state_vector[i].j5, state_vector[i].j6, state_vector[i].timestamp};
        js1[i] = state_vector[i].j1;
        js2[i] = state_vector[i].j2;
        js3[i] = state_vector[i].j3;
        js4[i] = state_vector[i].j4;
        js5[i] = state_vector[i].j5;
        js6[i] = state_vector[i].j6;
        jstimestamp[i] = state_vector[i].timestamp;

    }

    json out_js;
    out_js["J1"] = js1;
    out_js["J2"] = js2;
    out_js["J3"] = js3;
    out_js["J4"] = js4;
    out_js["J5"] = js5;
    out_js["J6"] = js6;
    out_js["timestamp"] = jstimestamp;
    std::ofstream o(out_cont);

    o << std::setw(4) << out_js << std::endl; // Conversion y envío de resultados en json
    o.close();

    // for (int k = 0; k < 6; k++)
    // {
    //     free(pjx[k]);
    // }

    return 0;
}
