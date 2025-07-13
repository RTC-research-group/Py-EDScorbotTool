#include <string>
#include "nlohmann/json.hpp"
#include <map>
#include <thread>
#define SPIKE_GEN_FREQ_DIVIDER 0x01
#define REF_ADDR 0x02
#define PI_FD_ENABLE_ADDR 0x03
#define PI_FD_ADDR 0x07
#define PD_FD_ENABLE_ADDR 0x08
#define PD_FD_ADDR 0x0c
#define SPIKE_EXPANSOR_ADDR 0x12
#define EI_FD_ENABLE_ADDR 0x13
#define EI_FD_ADDR 0x17
#define JOINT_STEP 0x20

// using namespace std;
using json = nlohmann::json;

static std::map<std::string, int> addresses = {
    {"M1", 0x00},
    {"M2", 0x20},
    {"M3", 0x40},
    {"M4", 0x60},
    {"M5", 0x80},
    {"M6", 0xA0}};

// Data structure to hold SPID configuration for 1 joint

/**
 * @brief  Class to implement joint functionalities
 *
 */
class EDScorbotJoint
{

private:
    // Declaring
    std::thread *t;

public:
    int address;
    int jnum;
    std::string id;
    std::map<std::string, int> controller = {
        {"EI_FD_bank3_18bits", 0},
        {"PD_FD_bank3_22bits", 0},
        {"PI_FD_bank3_18bits", 0},
        {"leds", 0},
        {"ref", 0},
        {"spike_expansor", 0}};

    /**
     * @brief Construct a new EDScorbotJoint object specifying each parameter
     *
     * @param EI_FD
     * @param PD_FD
     * @param PI_FD
     * @param leds
     * @param spike_exp
     * @param address
     * @param id
     */
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
    /**
     * @brief Construct a new EDScorbotJoint object specifing motor ID and joint number (1-6)
     * 
     * This constructor allows for later initialization of the joint's parameters
     * 
     * @param id String identifying joint/motor 
     * @param jnum Number identifying joint/motor. Used for indexing
     */
    EDScorbotJoint(std::string id, int jnum)
    {
        this->id = id;
        this->address = addresses[id];
        this->jnum = jnum;
    }
    /**
     * @brief Default destructor for EDScorbotJoint class
     * 
     */
    ~EDScorbotJoint(){};
    void configureInit();//Eliminable
    void configureSPID();//Eliminable
};

/**
 * @brief Class that handles communication with EDScorbot's controller in the FPGA
 * @details This class makes use of the underlying register-memory mapping that the MPSoC is able to provide. From the ARM point of view, 7 32-bit registers are available,
 * 1 write register used for control of each joint's controller and 6 read registers which hold the position of each joint at any given moment. From the FPGA point of view,
 * the register's use is inverted, thus having 1 read register and 6 write registers. The read register will contain 24-bit packets of data (packaged in 32 bits, so the 8 most significant
 * are discarded) that are able to command each joint's controller individually. The write registers are directly mapped to the counter registers that receive the optic encoders' signal.
 */

class EDScorbot
{

public:
    /*! \name This will be the description for the following group of variables
          It can be arbitrarily long, but the first line will show up in bold,
          and any subsequent lines will show up like a description under it
    */
    ///@{
    /** Joint initialization for EDScorbot handler */
        EDScorbotJoint j1 = {"M1", 1}, j2 = {"M2", 2}, j3 = {"M3", 3}, j4 = {"M4", 4}, j5 = {"M5", 5}, j6 = {"M6", 6};
    ///@}

    /**
     * @brief Construct a new EDScorbot object
     * 
     */

    EDScorbot(); //Eliminable?
    /**
     * @brief Construct a new EDScorbot object and initializes configuration for SPID controllers of EDScorbot
     *        
     * This constructor populates each joint's object variable with the parameters it needs to configure the underlying controller implementation.
     * 
     * @param config_path relative path to json configuration file. 
     * 
     */

    EDScorbot(std::string);

    /**
     * @brief Default destructor for EDScorbot class
     * 
     */

    ~EDScorbot();

    /**
     * @brief Explicitly initialize joint 1-6 configuration using loaded json config file
     * 
     */
    void initJoints();
    void configureInit();//Eliminable, realmente initJoints hace el trabajo
    void configureSPID(EDScorbotJoint);//Eliminable
    void configureInit(EDScorbotJoint);//Eliminable
    /**
     * @brief Initialize joint configuration for the specified joint
     * @param j Joint to be initialized
     */
    void configureInitJoint(EDScorbotJoint);
    /**
     * @brief Home routine, to be performed per joint
     * 
     * This function performs the home routine for a specific joint, indicated in the j parameter. Usually, a joint is commanded to move until it hits one of its
     * mechanical limits and then a gradual increase in position allows for searching the home signal, given by a microswitch in each joint
     * 
     * @param j Joint to perform the home routine to
     * @param v Whether to behave verbosely or not
     */
    void searchHome(EDScorbotJoint,bool);

    /**
     * @brief Command a specific position to a specific joint
     * 
     * 
     * @param ref Reference (position) to be commanded
     * @param j Joint to be commanded the reference `ref`
     */
    int sendRef(int, EDScorbotJoint);

    /**
     * @brief 
     * 
     */
    void resetCounter(EDScorbotJoint);//Eliminable
    void configureLeds(int, EDScorbotJoint);//Eliminable
    void sendFPGAReset();//Eliminable
    void loadConfig(std::string);//Eliminable
    void dumpConfig(std::string);//Eliminable
    /**
     * @brief Reset the controller's home position (reference 0) for a specific joint
     * 
     * @param j Joint which we want to reset the position of
     */
    void resetJPos(EDScorbotJoint);

    /**
     * @brief Implements counter register value to position in angles transformation
     * 
     * @param motor Joint/Motor for which to perform the conversion (different joints have different conversion values)
     * @param count Value read from the robot's counter register, which indicates absolute position of the joint
     * @return float Converted position value in angles (not radians) for the specified joint
     */
    float count_to_angle(int, int);

    /**
     * @brief Implements digital reference to counter register transformation
     * 
     * @param motor Joint/Motor for which to perform the conversion (different joints have different conversion values)
     * @param ref Value to be converted
     * @return int  Converted position value in 16-bit format, centered at 32768
     */
    static int ref_to_count(int, int);

    /**
     * @brief Implements counter register value to position in digital reference transformation
     * 
     * @param motor Joint/Motor for which to perform the conversion (different joints have different conversion values)
     * @param count Value read from the robot's counter register, which indicates absolute position of the joint
     * @return int Converted position
     */
    static int count_to_ref(int, int);

    /**
     * @brief Implements angle position to digital reference transformation
     * 
     * @param motor Joint/Motor for which to perform the conversion (different joints have different conversion values)
     * @param angle Value to be converted from position in angles to digital reference
     * @return int Converted position
     */
    static int angle_to_ref(int, float);

    /**
     * @brief  Implements digital reference to angle position transformation
     * 
     * @param motor Joint/Motor for which to perform the conversion (different joints have different conversion values)
     * @param ref Value to be converted from digital reference to position in angles
     * @return float Converted position in angles (not radians)
     */
    static float ref_to_angle(int, int);

#ifdef THREADED
    void EDScorbot::readJoints();
    bool exec;
#else
/**
 * @brief Function to read the state of all the robot's joints
 * 
 * This function receives an integer array of 6 elements and assigns each of them the value of one of the robot's joints. As such, if `joints` is the name of the array, 
 * `joints[0]` will hold the position of joint 1, `joints[1]` will hold the position of joint 2, etc., up to `joints[5]`, which would hold the position of joint 6
 * 
 * @param joints [in,out] Array of six integers, to be filled with each joint's position per element
 */
    void readJoints(int *);
#endif
private:
    int *bram_ptr; //!< Pointer to the base memory address in which the FPGA registers are placed
};