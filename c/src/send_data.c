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

int sendCommand16(uchar addr, uchar b1, uchar b2, int *mem, int verbose)
{
    int data = 0x000000 | addr << 16 | b1 << 8 | b2;
    if (verbose)
    {
        printf("Datos: %08x\n", data);
    }
    mem[0] = data;
    return 0;
}

int main()
{
    unsigned int bram_size = 0xFF;
    off_t bram_pbase = 0x43c00000; // physical base address
    int *bram64_vptr;
    int fd;

    // Map the BRAM physical address into user space getting a virtual address for it
    if ((fd = open("/dev/mem", O_RDWR | O_SYNC)) != -1)
    {

        bram64_vptr = (int *)mmap(NULL, bram_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, bram_pbase);

        // Write to the memory that was mapped, use devmem from the command line of Linux to verify it worked
        // it could be read back here also

        //  bram64_vptr[0] = 0xDEADBEEF;
        // int test = *(bram64_vptr);
        // printf("Leido: %x\n",test);

        puts("/dev/mem abierto correctamente");
        close(fd);
    }
    else
    {
        puts("Ocurrió un problema al abrir /dev/mem");
    }
    clock_t start = clock();
    sendCommand16(0x02, 0x43, 0xff, bram64_vptr, 0);
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("Tiempo en ejecutar el comando: %f segundos\n",seconds);
    return 0;
}