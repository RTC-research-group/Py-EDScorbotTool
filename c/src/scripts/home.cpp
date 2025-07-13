#include "include/EDScorbot.hpp"
#include <time.h>
#include <unistd.h>
#include <argparse/argparse.hpp>


int main(int argc, char* argv[])
{   
    
    argparse::ArgumentParser parser("reset");
    parser.add_argument("-c", "--config_file").help("Optional. Configuration file in JSON format. This file can be used to configure each joint's controller parameters. Default is 'initial_config.json'").default_value(std::string("initial_config.json"));
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
    bool verbose = parser.get<bool>("--verbose");
    EDScorbot handler(config_file);

    EDScorbotJoint *joint;

    handler.initJoints();

    puts("J3");
    handler.searchHome(handler.j3,verbose);
    puts("J2");
    handler.searchHome(handler.j2,verbose);
    puts("J1");
    handler.searchHome(handler.j1,verbose);
 
    puts("Waiting for PID to stabilize");
    usleep(15000000);
    EDScorbotJoint *joints[6] = {&handler.j1, &handler.j2, &handler.j3, &handler.j4, &handler.j5, &handler.j6};

    int i;
    for (i = 0; i < 4; i++)
    {
        handler.resetJPos(*joints[i]);
    }
    // int reads[6];
    // handler.readJoints(reads);

    // puts("Leido:");
    // for (int i = 0;i<6; i++){
    //     printf("J%d: %d\n",i+1,reads[i]);
    // }

    return 0;
}