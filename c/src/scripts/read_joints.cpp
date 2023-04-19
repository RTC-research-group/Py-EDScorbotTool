#include "include/EDScorbot.hpp"


int main(int argc, char *argv[])
{
    int j = atoi(argv[1]);
    int ref = atoi(argv[2]);
    int init = atoi(argv[3]);
    char *config_file = argv[4];
    EDScorbot handler(config_file);

    EDScorbotJoint *joint;
    switch (j)
    {
    case 1:
        joint = &handler.j1;
        break;
    case 2:
        joint = &handler.j2;
        break;
    case 3:
        joint = &handler.j3;
        break;
    case 4:
        joint = &handler.j4;
        break;
    case 5:
        joint = &handler.j5;
        break;
    case 6:
        joint = &handler.j6;
        break;

    default:
        break;
    }
    if (init)
        handler.initJoints();

    handler.sendRef(ref, *joint);
    char c = 'a';
    int reads[6];

    while (c != EOF)
    {
        handler.readJoints_counter(reads);
        printf("J%d: %d\tJ%d: %d\tJ%d: %d\tJ%d: %d\tJ%d: %d\tJ%d: %d\t\r", 1, reads[0],2, reads[1],3, reads[2],4, reads[3],5, reads[4],6, reads[5]);
        fflush(stdout);
    
    }

    return 0;
}