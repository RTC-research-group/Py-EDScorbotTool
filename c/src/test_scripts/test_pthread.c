#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

void * func(void* arg){
    printf("principio");
    usleep(1000000);
    printf("final");
    return NULL;
}

int main(){

    pthread_t t;
    int err = pthread_create(&t,NULL,&func,NULL);
    pthread_detach(t);

    puts("main");
    usleep(1000000);
    
    puts("main");
    usleep(1000000);
    puts("main");

    return 0;
}