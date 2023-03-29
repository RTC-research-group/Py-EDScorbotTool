#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>


int main(int argc, char* argv[])
{   
    
    
    int r = putenv("HOME_EXEC=1");
    printf("HOME_EXEC=1, result: %d\n",r);
    fflush(stdout);
    sleep(5);
    char* r2 = getenv("HOME_EXEC");
    printf("HOME_EXEC getenv: %s\n",r2);
    fflush(stdout);
    
    r = putenv("HOME_EXEC=0");
    printf("HOME_EXEC=0, result: %d\n",r);
    fflush(stdout);
     
    r2 = getenv("HOME_EXEC");
    printf("HOME_EXEC getenv: %s\n",r2);
    fflush(stdout);
    return 0;
}