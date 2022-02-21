#include "include/EDScorbot.hpp"
#include <nlohmann/json.hpp>
#include <iostream>
#include <fstream>
#include <string>
#include <map>

using namespace std;
using json = nlohmann::json;


// void EDScorbotJoint::setEI_FD(int EI_FD){

// };

EDScorbot::EDScorbot()
{

    string config_path = "/home/enrique/Trabajo/Py-EDScorbotTool/c/src/initial_config.json";
    ifstream config_file(config_path, ios::in);
    json config = json::parse(config_file);
    json motor_config = config["Motor Config"];

    array<EDScorbotJoint,6> joints = {{j1,j2,j3,j4,j5,j6}};
    int ei_fd = motor_config["EI_FD_bank3_18bits_M1"];
    int pd_fd = motor_config["PD_FD_bank3_22bits_M1"];

    for(auto& j:joints){
        cout << j.controller.id;
    }

    // for (auto& x : motor_config.items())
    // {
    //   //  int a = x.value();
    //     std::cout << "key: " << x.key() << ", value: " << x.value() << '\n';
    // }
    int b = 1;

};

int main()
{
    printf("Hello world\n");
    EDScorbot handler;
    return 0;
}