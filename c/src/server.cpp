#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include "include/EDScorbot.hpp"
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#define MAX_BYTES 1500
#define SERVER_PORT htons(9999)

int printJson(const char *json);

int main(int argc, char *argv[])
{
    // Buffer for incoming data
    char buffer[MAX_BYTES];
    // We will store return values of functions in n
    int n;
    // Server socket
    int serverSock = socket(AF_INET, SOCK_STREAM, 0);

    // Socket config struct
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = SERVER_PORT;
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    /* bind (this socket, local address, address length)
       bind server socket (serverSock) to server address (serverAddr).
       Necessary so that server can use a specific port */
    bind(serverSock, (struct sockaddr *)&serverAddr, sizeof(struct sockaddr));
    while (1)
    {   
        // wait for a client
        /* listen (this socket, request queue length) */
        listen(serverSock, 1);

        // Ip of client
        sockaddr_in clientAddr;
        socklen_t sin_size = sizeof(struct sockaddr_in);
        // Accept incoming connection
        int clientSock = accept(serverSock, (struct sockaddr *)&clientAddr, &sin_size);

        int go = 0;
        do
        {
            bzero(buffer, MAX_BYTES);

            // receive a message from a client
            n = read(clientSock, buffer, MAX_BYTES);
            // cout << "Confirmation code  " << n << endl;
            // cout << "Server received:  " << buffer << endl;
#ifdef EDS_VERBOSE
            printJson(buffer);
#endif
            // Añadir maquina de estados
            int estado = 0;
            for (int i = 0; i < strlen(buffer);i++){
                char c = buffer[i];
                switch(estado){
                    
                    case 0:break;

                    default:break;

                }
            }

            if (strcmp(buffer, "refJ1 50") == 0)
            {
                puts("blop");
                // handler.sendRef(50,handler.j1);
            }

            strcpy(buffer, "test");
            n = write(clientSock, buffer, strlen(buffer));
            std::cout << "Confirmation code  " << n << std::endl;
        } while (go);
    }
    return 0;
};

int printJson(const char *json)
{
    FILE *f = fopen("./tmp_config.json", "w");
    int written = fprintf(f, "%s", json);
    fclose(f);
    return written;
};