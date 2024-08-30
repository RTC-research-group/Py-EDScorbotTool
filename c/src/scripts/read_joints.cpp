#include "trajectory/utils.h"



int main(int argc, char *argv[])
{
    argparse::ArgumentParser parser("read_joints");
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

    const char *config_file = parser.get<std::string>("--config_file").c_str();
    mosquitto_lib_init();
    usleep(10000000); // Wait for 10 seconds to let the arm come back to home position
    struct mosquitto *mosq;
    mosq = mosquitto_new(NULL, true, 0);
    char ip[20] = "192.168.1.104";
    init_mqtt_client(mosq, ip);
    char mqtt_msg[MAX_MQTT_MSG];
    EDScorbot handler(config_file);
   
    
    char c = 'a';
    int reads[6];

    while (c != EOF)
    {
        handler.readJoints_counter(reads);
        // printf("J%d: %d\tJ%d: %d\tJ%d: %d\tJ%d: %d\tJ%d: %d\tJ%d: %d\t\r", 1, reads[0],2, reads[1],3, reads[2],4, reads[3],5, reads[4],6, reads[5]);
        snprintf(mqtt_msg,MAX_MQTT_MSG,"[%d,%d,%d,%d,%d,%d]", reads[0], reads[1], reads[2], reads[3], reads[4], reads[5]);
        int ret = publish(mosq, mqtt_msg, strlen(mqtt_msg), std::string("EDScorbot/trajectory").c_str());

        fflush(stdout);
        usleep(100000);
        
        
    
    }

    return 0;
}