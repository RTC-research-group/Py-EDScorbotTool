#include "include/EDScorbot.hpp"


int main(int argc, char* argv[])
{   
    int j = atoi(argv[1]);
    int ref = atoi(argv[2]);
    int init = atoi(argv[3]);
    EDScorbot handler("./initial_config.json");
    EDScorbotJoint* joint;
    switch (j)
    {
    case 1:joint = &handler.j1;break;
    case 2:joint = &handler.j2;break;
    case 3:joint = &handler.j3;break;
    case 4:joint = &handler.j4;break;
    case 5:joint = &handler.j5;break;
    case 6:joint = &handler.j6;break;
    
    default:
        break;
    }
    if(init)
        handler.initJoints();

    handler.sendRef(ref,*joint);
    array<int,6> reads = handler.readJoints();

    puts("Leido:");
    for (int i = 0;i<6; i++){
        printf("J%d: %d\n",i+1,reads[i]);
    }

    

    return 0;

}