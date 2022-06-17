#include <iostream>
#include <fstream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#define MAX_BYTES 1500
#define SERVER_PORT htons(9998)

int fprintJson(const char *json);
int fprintTrajectory(const char *tray, int len);
int write_file(const char* fname, unsigned char* fdata);

int main(int argc, char *argv[])
{

    // Buffer for incoming data
    unsigned char file_name_buf[MAX_BYTES];
    unsigned char file_buf[MAX_BYTES];
    char command_buf[10];
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
            bzero(file_buf, MAX_BYTES);
            bzero(file_name_buf, MAX_BYTES);

            // receive a message from a client

            // cout << "Confirmation code  " << n << endl;
            // cout << "Server received:  " << buffer << endl;

            // Añadir maquina de estados
            char w_buffer[10] = "[OK]";
            int n_filename = read(clientSock, file_name_buf, MAX_BYTES);
            int n_send = write(clientSock, w_buffer, strlen(w_buffer));
            
            usleep(10000);
            int n_file = read(clientSock, file_buf, MAX_BYTES);
            n_send = write(clientSock, w_buffer, strlen(w_buffer));

            usleep(10000);
            int n_command = read(clientSock, command_buf, 10);
            n_send = write(clientSock, w_buffer, strlen(w_buffer));

            int command = atoi(command_buf);

            switch(command){
                //Receive file and end
                case 1: break;
                //Receive trajectory and execute it
                case 2: write_file(file_name_buf,file_buf,n_file);
                        char cmd[256];
                        sprintf(cmd,"bash ./exec %s",file_name_buf);
                        system(cmd);
                        
                        break;
                
                default: break;
            }

            
            // Seguir probando
            // Ref de 1 en 1 --> [3] ; [j,ref]

            // if (strcmp(buffer, "[4]") == 0)
            // {
            //     // Enviar trayectoria --> [4]
            //     char w_buffer[10] = "[OK]";
            //     n = write(clientSock, w_buffer, strlen(w_buffer));
            //     usleep(10000);
            //     char len_buffer[20];
            //     n = read(clientSock, buffer, MAX_BYTES);
            //     fprintTrajectory(buffer, n);
            //     // Probar que esto funciona y que se abre el .npy correctamente
            // }

            // if (strcmp(buffer, "[5]") == 0)
            // {
            //     // Enviar .json configuracion --> [5] ; datos
            //     char w_buffer[10] = "[OK]";
            //     n = write(clientSock, w_buffer, strlen(w_buffer));
            //     usleep(10000);
            //     n = read(clientSock, buffer, MAX_BYTES);
            //     fprintJson(buffer);
            // }

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

int fprintTrajectory(const char *tray, int len)
{
    // FILE *f = fopen("./tmp_tray.npy", "wb");
    // int written = fprintf(f, "%s", tray);
    // fclose(f);
    // return written;

    std::ofstream f;
    f.open("./tmp_tray.npy", std::ios_base::out | std::ios_base::binary | std::ios_base::trunc);
    std::string str(tray, len);

    f << str;
    f.close();
    int a = 1;
    return 0;
};

int write_file(const char* fname, unsigned char* fdata,int flen){
    FILE *f = fopen((const char*)file_name_buf, "wb");
            int len = fwrite((const void *)(file_buf), 1, flen, f);

            //printf("%s writen\n",file_name_buf);
            printf("Writen %d bytes to file %s\n",len,file_name_buf);
            fclose(f);
}