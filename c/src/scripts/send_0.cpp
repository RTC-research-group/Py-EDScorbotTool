/** @file send_0.cpp
*/ 

#include "include/EDScorbot.hpp"

/**
 * @brief This is a CLI util to be used whithin the Zynq's environment. It sends all joints to their home position (reference 0). Invocation without parameters or with -help/-h flag will print a help message.
 * 
 * @param config_file Configuration file to use, in JSON format. This file can be used to configure each joint's controller parameters. Default is 'initial_config.json'.
 * @param verbose Choose verbosity of output. Only True/False can be used.
 */
int main(int argc, char* argv[])
{   
    //int j = atoi(argv[1]);
    //int ref = atoi(argv[2]);
    //int init = atoi(argv[3]);
    char* config_file = argv[1];
    EDScorbot handler(config_file);
    
    EDScorbotJoint* joint;
    // switch (j)
    // {
    // case 1:joint = &handler.j1;break;
    // case 2:joint = &handler.j2;break;
    // case 3:joint = &handler.j3;break;
    // case 4:joint = &handler.j4;break;
    // case 5:joint = &handler.j5;break;
    // case 6:joint = &handler.j6;break;
    
    // default:
    //     break;
    // }
   // if(init)
    handler.sendRef(0,handler.j1);
    handler.sendRef(0,handler.j2);
    handler.sendRef(0,handler.j3);
    handler.sendRef(0,handler.j4);

    // puts("J1");
    // handler.searchHome(handler.j1);
    // puts("J2");
    // handler.searchHome(handler.j2);
    // puts("J3");
    // handler.searchHome(handler.j3);
    // puts("J4");
    // handler.searchHome(handler.j4);
    
    // int reads[6];
    // handler.readJoints(reads);

    // puts("Leido:");
    // for (int i = 0;i<6; i++){
    //     printf("J%d: %d\n",i+1,reads[i]);
    // }

    

    return 0;

}