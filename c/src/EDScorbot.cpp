#include "include/EDScorbot.hpp"
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include "include/devmem.hpp"

using namespace std;
using json = nlohmann::json;

// Constructor
// string config_path -> relative path to json configuration file
// Initializes configuration for SPID controllers of EDScorbot
EDScorbot::EDScorbot(string config_path)
{

    /*
    ***********************************
        Joint configuration
    ***********************************
    */
    // Open config file
    ifstream config_file(config_path, ios::in);
    // Parse with json library
    json config = json::parse(config_file);
    // Take what we need -- check initial_config.json to see data structure
    json motor_config = config["Motor Config"];

    // Automatic configuration for SPID controllers
    // We iterate through the json motor config dictionary
    for (const auto &[k, v] : motor_config.items())
    {
        // Check to which motor the key corresponds
        bool m1, m2, m3, m4, m5, m6;
        // Keys have format XX_XX_...._MJ, with J ={1,2,3,4,5,6}
        m1 = (k.find("M1") != std::string::npos);
        m2 = (k.find("M2") != std::string::npos);
        m3 = (k.find("M3") != std::string::npos);
        m4 = (k.find("M4") != std::string::npos);
        m5 = (k.find("M5") != std::string::npos);
        m6 = (k.find("M6") != std::string::npos);

        // Remove MJ from keys, internal keys for the controller are motor-agnostic
        string subk = k.substr(0, k.size() - 3);
        // Assign each key its corresponding value
        if (m1)
        {
            j1.controller[subk] = v;
        }

        if (m2)
        {
            j2.controller[subk] = v;
        }

        if (m3)
        {
            j3.controller[subk] = v;
        }

        if (m4)
        {
            j4.controller[subk] = v;
        }

        if (m5)
        {
            j5.controller[subk] = v;
        }

        if (m6)
        {
            j6.controller[subk] = v;
        }
    }
    // Create array to iterate over joints
    array<EDScorbotJoint *, 6> joints = {{&j1, &j2, &j3, &j4, &j5, &j6}};

    for (const auto &j : joints)
    { // Assign each joint its correct address -- 0x00,0x20,...,0xA0
        j->address = addresses[j->id];
#ifdef EDS_VERBOSE
        // print controller configuration if verbose
        int i = 1;
        cout << "J" << i << "\n";
        i = i + 1;
        for (const auto &[k, v] : j->controller)
        {
            cout << "Key: " << k << " Valor: " << v << "\n";
        }
#endif
    }

    /*
***********************************
    BRAM config for write/read
***********************************
*/

    int *bram_ptr = open_devmem();
    this->bram_ptr = bram_ptr;
};

int EDScorbot::sendRef(int ref, EDScorbotJoint j)
{   
    uchar offset = 0x02;
    uchar address = j.address + offset;
    uchar b1 = ((ref >> 8) & 0xFF);
    uchar b2 = ref & 0xFF;
    sendCommand16(address,b1,b2,this->bram_ptr);
    return 0;
}

array<int,6> EDScorbot::readJoints(){
    //int base_address = 0x00;//To be defined
    //int offset = 0x20;

    int j1,j2,j3,j4,j5,j6;

    j1 = this->bram_ptr[0];
    j2 = this->bram_ptr[0];
    j3 = this->bram_ptr[0];
    j4 = this->bram_ptr[0];
    j5 = this->bram_ptr[0];
    j6 = this->bram_ptr[0];

    array <int,6> ret = {j1,j2,j3,j4,j5,j6};
    return ret;

};