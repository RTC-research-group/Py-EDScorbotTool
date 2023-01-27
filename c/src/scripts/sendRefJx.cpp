#include "include/EDScorbot.hpp"
#include <argparse/argparse.hpp>

int main(int argc, char *argv[])
{
    argparse::ArgumentParser parser("sendRef");
    parser.add_argument("joint").help("Joint to be moved. Integer").scan<'i', int>();
    parser.add_argument("ref").help("Digital reference to be commanded to the joint. Integer").scan<'i', int>();
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

    int ref = parser.get<int>("ref");
    int j = parser.get<int>("joint");
    const char *config_file = parser.get<std::string>("--config_file").c_str();
    bool verbose = parser.get<bool>("--verbose");
    
    EDScorbot handler(config_file);

    EDScorbotJoint *joint;
    switch (j)
    {
    case 1:
        joint = &handler.j1;
        break;
    case 2:
        joint = &handler.j2;
        break;
    case 3:
        joint = &handler.j3;
        break;
    case 4:
        joint = &handler.j4;
        break;
    case 5:
        joint = &handler.j5;
        break;
    case 6:
        joint = &handler.j6;
        break;

    default:
        return -1;
    }

    handler.sendRef(ref, *joint);

    return 0;
}