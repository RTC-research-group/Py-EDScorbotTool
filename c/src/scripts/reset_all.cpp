/** @file reset_all.cpp
*/ 
#include "include/EDScorbot.hpp"

#include <argparse/argparse.hpp>

/**
 * @brief This is a CLI util to be used whithin the Zynq's environment. Sets current position of each joint to be their 'Home' position (i.e. the position they will go to if the controller is given a reference value of 0). Invocation without parameters or with -help/-h flag will print a help message.
 * 
 * @param config_file Configuration file to use, in JSON format. This file can be used to configure each joint's controller parameters. Default is 'initial_config.json'.
 * @param verbose Choose verbosity of output. Only True/False can be used.
 */
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
    
    EDScorbotJoint* joint;

    handler.configureInitJoint(handler.j1);
    handler.configureInitJoint(handler.j2);
    handler.configureInitJoint(handler.j3);
    handler.configureInitJoint(handler.j4);

    

    return 0;

}