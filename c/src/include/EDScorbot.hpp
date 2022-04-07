#include <string>
#include "nlohmann/json.hpp"
#include <map>
#include <thread>
#define REF_ADDR 0x02   
#define PI_FD_ENABLE_ADDR 0x03
#define PI_FD_ADDR 0x07
#define PD_FD_ENABLE_ADDR 0x08
#define PD_FD_ADDR 0x0c
#define SPIKE_EXPANSOR_ADDR 0x12
#define EI_FD_ENABLE_ADDR 0x13
#define EI_FD_ADDR 0x17
#define JOINT_STEP 0x20


//using namespace std;
using json = nlohmann::json;

static std::map<std::string, int> addresses = {
        {"M1", 0x00},
        {"M2", 0x20},
        {"M3", 0x40},
        {"M4", 0x60},
        {"M5", 0x80},
        {"M6", 0xA0}};


// Data structure to hold SPID configuration for 1 joint


// Class to implement joint functionalities
class EDScorbotJoint
{

private:
    // Declaring
    std::thread* t;
public:
    int address;
    std::string id;
    std::map<std::string, int> controller = {
        {"EI_FD_bank3_18bits", 0},
        {"PD_FD_bank3_22bits", 0},
        {"PI_FD_bank3_18bits", 0},
        {"leds", 0},
        {"ref", 0},
        {"spike_expansor", 0}};


    EDScorbotJoint(int EI_FD, int PD_FD, int PI_FD, int leds, int spike_exp, int address, std::string id)
    {
        controller["EI_FD_bank3_18bits"] = EI_FD;
        controller["PD_FD_bank3_22bits"] = PD_FD;
        controller["PI_FD_bank3_18bits"] = PI_FD;
        controller["leds"] = leds;
        controller["ref"] = 0;
        controller["spike_expansor"] = spike_exp;
        this->id = id;
        this->address = addresses[id];
    };
    EDScorbotJoint(std::string id)
    {
        this->id = id;
        this->address = addresses[id];
    }
    ~EDScorbotJoint(){};
    void configureInit();
    void configureSPID();

};

class EDScorbot
{

private:

    int* bram_ptr;

public:
    EDScorbotJoint j1 = {"M1"}, j2 = {"M2"}, j3 = {"M3"}, j4 = {"M4"}, j5 = {"M5"}, j6 = {"M6"};

    EDScorbot();
    EDScorbot(std::string);
    ~EDScorbot();
    void initJoints();
    void configureInit();
    void configureSPID(EDScorbotJoint);
    void configureInit(EDScorbotJoint);
    void searchHome(EDScorbotJoint);
    int sendRef(int, EDScorbotJoint);
    void resetCounter(EDScorbotJoint);
    void configureLeds(int, EDScorbotJoint);
    void sendFPGAReset();
    void loadConfig(std::string);
    void dumpConfig(std::string);
#ifdef THREADED
    void EDScorbot::readJoints();
    bool exec;
#else
    void readJoints(int*);
#endif
    
};