extern "C"{
#include "include/devmem.hpp"


int sendCommand16(uchar addr, uchar b1, uchar b2, int *mem)
{
    int data = 0x000000 | addr << 16 | b1 << 8 | b2;
#ifdef EDS_VERBOSE
    {
        printf("Datos: %08x\n", data);
    }
#endif
    mem[0] = data;
    return 0;
}

int *open_devmem()
{
    unsigned int bram_size = 0xFF;
    off_t bram_pbase = 0x44000000; // physical base address
    int *bram_ptr;
    int fd;

    // Map the BRAM physical address into user space getting a virtual address for it
    if ((fd = open("/dev/mem", O_RDWR | O_SYNC)) != -1)
    {

        bram_ptr = (int *)mmap(NULL, bram_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, bram_pbase);

        // Write to the memory that was mapped, use devmem from the command line of Linux to verify it worked
        // it could be read back here also

        //  bram64_vptr[0] = 0xDEADBEEF;
        // int test = *(bram64_vptr);
        // printf("Leido: %x\n",test);

        puts("/dev/mem opened correctly");
        close(fd);
    }
    else
    {
        puts("Something happened while trying to open /dev/mem");
    }

    return bram_ptr;
}

}