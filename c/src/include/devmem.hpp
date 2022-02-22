extern "C"{
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <time.h>

// Make the SDK console work in the debugger
#define printf(...)               \
    fprintf(stdout, __VA_ARGS__); \
    fflush(stdout);

typedef long long int u64;
typedef unsigned char uchar;

int sendCommand16(uchar addr, uchar b1, uchar b2, int *mem);

int *open_devmem();

}