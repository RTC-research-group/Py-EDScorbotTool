#include <string>
#include "nlohmann/json.hpp"
#include <map>

using namespace std;
using json = nlohmann::json;

map<string, int> addresses = {
    {"M1", 0x00},
    {"M2", 0x20},
    {"M3", 0x40},
    {"M4", 0x60},
    {"M5", 0x80},
    {"M6", 0xA0}};

// Data structure to hold SPID configuration for 1 joint
typedef struct controller
{
    int EI_FD_bank3_18bits;
    int PD_FD_bank3_22bits;
    int PI_FD_bank3_18bits;
    int leds;
    int ref;
    int spike_expansor;
    string address;
    string id;

} SPIDController;

// Class to implement joint functionalities
class EDScorbotJoint
{

private:
    // Declaring

public:
    SPIDController controller;//Dejar privado? En ese caso habria que hacer getters y setters :(

    EDScorbotJoint(){};
    EDScorbotJoint(int EI_FD, int PD_FD, int PI_FD, int leds, int spike_exp, string address, string id)
    {
        controller.EI_FD_bank3_18bits = EI_FD;
        controller.PD_FD_bank3_22bits = PD_FD;
        controller.PI_FD_bank3_18bits = PI_FD;
        controller.leds = leds;
        controller.ref = 0;
        controller.spike_expansor = spike_exp;
        controller.address = address;
        controller.id = id;
    };
    EDScorbotJoint(string id)
    {
        controller.id = id;
        controller.address = addresses[id];
    }
    ~EDScorbotJoint(){};
    void configureInit();
    void configureSPID();
    // void setControllerConfig(int, int, int, int, int, string, string);
    // void setEI_FD(int);
    // void setPD_FD(int);
    // void setPI_FD(int);
    // void setLeds(int);
    // void setRef(int);
    // void setSpikeExpansor(int);
    // void getMotorAddress();
    // void getId(int);
    // void getControllerConfig(int, int, int, int, int, string, string);
    // void getEI_FD(int);
    // void getPD_FD(int);
    // void getPI_FD(int);
    // void getLeds(int);
    // void getRef(int);
    // void getSpikeExpansor(int);
    // void getMotorAddress(int);
    // void getId(int);
};

class EDScorbot
{

private:
    EDScorbotJoint j1 = {"M1"}, j2 = {"M2"}, j3 = {"M3"},j4 = {"M4"},j5 = {"M5"},j6 = {"M6"};

public:
    EDScorbot();
    EDScorbot(string);
    ~EDScorbot(){};

    void configureSPID(EDScorbotJoint);
    void configureInit(EDScorbotJoint);
    void searchHome(EDScorbotJoint);
    void sendRef(int, EDScorbotJoint);
    int readJoint(EDScorbotJoint);
    void resetCounter(EDScorbotJoint);
    void configureLeds(int, EDScorbotJoint);
    void sendFPGAReset();
    void loadConfig(string);
    void dumpConfig(string);
};