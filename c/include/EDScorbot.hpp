#include <string>
#include "nlohmann/json.hpp"

using namespace std;
using json = nlohmann::json;

//Data structure to hold SPID configuration for 1 joint
typedef struct controller{
    int EI_FD_bank3_18bits;
    int PD_FD_bank3_22bits;
    int PI_FD_bank3_18bits;
    int leds;
    int ref;
    int spike_expansor;
    string motor_address;
    string id;

} SPIDController;


//Class to implement joint functionalities
class EDScorbotJoint{

    private:
    //Declaring 
        SPIDController controller;

    public:
        EDScorbotJoint();
        EDScorbotJoint(int EI_FD, int PD_FD,int PI_FD,int leds,int spike_exp, string address,string id){
            controller.EI_FD_bank3_18bits = EI_FD;
            controller.PD_FD_bank3_22bits = PD_FD;
            controller.PI_FD_bank3_18bits = PI_FD;
            controller.leds = leds;
            controller.ref = 0;
            controller.spike_expansor = spike_exp;
            controller.motor_address= address;
            controller.id = id;
        };
        ~EDScorbotJoint();
        void configureInit();
        void configureSPID();
        void setControllerConfig(int,int,int,int,int,string,string);
        void setEI_FD(int);
        void setPD_FD(int);
        void setPI_FD(int);
        void setLeds(int);
        void setRef(int);
        void setSpikeExpansor(int);
        void setMotorAddress(int);
        void setId(int);

};

class EDScorbot{

    private:
        EDScorbotJoint j1,j2,j3,j4,j5,j6;
    int addr;

    public:
        EDScorbot();
        EDScorbot(string);
        ~EDScorbot();

        
        void configureSPID(EDScorbotJoint);
        void configureInit(EDScorbotJoint);
        void searchHome(EDScorbotJoint);
        void sendRef(int,EDScorbotJoint);
        int readJoint(EDScorbotJoint);
        void resetCounter(EDScorbotJoint);
        void configureLeds(int, EDScorbotJoint);
        void sendFPGAReset();
        void loadConfig(string);
        void dumpConfig(string);

};