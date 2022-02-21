#include "include/EDScorbot.hpp"
#include "nlohmann/json.hpp"
#include <iostream>
#include <fstream>
#include <string>

using namespace std;
using json = nlohmann::json;

EDScorbot::EDScorbot(){

    string config_path = "./initial_config.json";
    ifstream config_file(config_path,ios::in);
    json config = json::parse(config_file); 
};