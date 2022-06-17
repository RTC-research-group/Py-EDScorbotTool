#include "nlohmann/json.hpp"
#include <map>
#include <iostream>
#include <fstream>
using json = nlohmann::json;

int main(int argc, char* argv[]){
    ifstream nparray(argv[1], ios::in);

     for (const auto &[k, v] : nparray.items()){
        cout << "Key: " << k << std::endl;
        cout << "Value: " << v << std::endl;
     }

    return 0;
}