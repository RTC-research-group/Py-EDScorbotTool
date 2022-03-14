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

int fprintJson(const char *json);
int fprintTrajectory(const char *tray);

int main(int argc, char *argv[])
{

    EDScorbot handler("./initial_config.json");
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
            fprintJson(buffer);
#endif
            // Añadir maquina de estados

            if (strcmp(buffer, "[0]") == 0)
            {
                char w_buffer[10] = "[OK]";
                n = write(clientSock, w_buffer, strlen(w_buffer));

                // handler.configureInit();
                //  handler.sendRef(50,handler.j1);
            }

            if (strcmp(buffer, "[1]") == 0)
            {
                char w_buffer[10] = "[OK]";
                n = write(clientSock, w_buffer, strlen(w_buffer));

                handler.initJoints();
            }

            if (strcmp(buffer, "[2]") == 0)
            {
                char w_buffer[10] = "[OK]";
                n = write(clientSock, w_buffer, strlen(w_buffer));

                // handler.resetCount();
            }

            if (strcmp(buffer, "[3]") == 0)
            {
                char w_buffer[10] = "[OK]";
                n = write(clientSock, w_buffer, strlen(w_buffer));
                usleep(10000);
                n = read(clientSock, buffer, MAX_BYTES);
                char delim = ',';
                char *j = (strtok(buffer, (const char *)delim));
                printf("char* j: %s\n", j);
                // Seguir probando
                // Ref de 1 en 1 --> [3] ; [j,ref]
            }

            if (strcmp(buffer, "[4]") == 0)
            {
                // Enviar trayectoria --> [4]
                char w_buffer[10] = "[OK]";
                n = write(clientSock, w_buffer, strlen(w_buffer));
                usleep(10000);
                n = read(clientSock, buffer, MAX_BYTES);
                fprintTrajectory(buffer);
                // Probar que esto funciona y que se abre el .npy correctamente
            }

            if (strcmp(buffer, "[5]") == 0)
            {
                // Enviar .json configuracion --> [5] ; datos
                char w_buffer[10] = "[OK]";
                n = write(clientSock, w_buffer, strlen(w_buffer));
                usleep(10000);
                n = read(clientSock, buffer, MAX_BYTES);
                fprintJson(buffer);
            }

            // strcpy(buffer, "test");
            // n = write(clientSock, buffer, strlen(buffer));
            // std::cout << "Confirmation code  " << n << std::endl;
        } while (go);
    }

    return 0;
};

int fprintJson(const char *json)
{
    FILE *f = fopen("./tmp_config.json", "w");
    int written = fprintf(f, "%s", json);
    fclose(f);
    return written;
};

int fprintTrajectory(const char *tray)
{
    FILE *f = fopen("./tmp_tray.npy", "wb");
    int written = fprintf(f, "%s", tray);
    fclose(f);
    return written;
};