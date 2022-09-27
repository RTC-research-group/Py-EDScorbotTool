#include <argparse/argparse.hpp>

int main(int argc, char *argv[])
{

    argparse::ArgumentParser parser("trajectory");
    parser.add_argument("trajectory_file").help("File which contains the trajectory in JSON format");
    parser.add_argument("n_points").help("Number of points of the trajectory. Integer").scan<'i', int>();
    parser.add_argument("-cont", "--out_cont").help("Optional. Base name of output files for counter values").default_value(std::string("out_cont"));
    parser.add_argument("-xyz", "--out_xyz").help("Optional. Base name of output files for xyz values").default_value(std::string("out_xyz"));

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

    

    printf("Valores parseados\ntrajectory_file:%s\nn_points:%d\n",jsonnp_array_fname,n);
}