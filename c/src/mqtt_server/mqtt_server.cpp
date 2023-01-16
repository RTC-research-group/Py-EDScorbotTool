#include <signal.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <cassert>
#include "mosquitto.h"

#define mqtt_host "192.168.1.104"
#define mqtt_port 1883

static int run = 1;
struct mosquitto *mosq;

typedef struct
{
	int type;
	char mode;
	char *payload;
	int last;
} progress_info;

progress_info progress;

void parse_command(char *command, int *t, char *m, char *url, int *n);
void ftp_trajectory(char *url);
void handle_signal(int s)
{
	run = 0;
}

void connect_callback(struct mosquitto *mosq, void *obj, int result)
{
	printf("connect callback, rc=%d\n", result);
}

void message_callback(struct mosquitto *mosq, void *obj, const struct mosquitto_message *message)
{
	bool match = 0;
	// printf("got message '%.*s' for topic '%s'\n", message->payloadlen, (char*) message->payload, message->topic);

	mosquitto_topic_matches_sub("/EDScorbot/commands", message->topic, &match);
	if (match)
	{
#ifdef EDS_VERBOSE
		printf("got message for /EDScorbot/commands topic\n");
#endif

		int type, n;
		char mode;
		char url[100];
		parse_command((char *)message->payload, &type, &mode, url, &n);
		progress.type = type;
		progress.mode = mode;
		progress.payload = url;
		progress.last = 1;
		char *cmd, *out_fname;
		switch (progress.type)
		{
		case 1:
			// Trajectory
			if (progress.mode == 'S')
			{
				cmd = reinterpret_cast<char *>(malloc(512));
				out_fname = reinterpret_cast<char *>(malloc(100));
				int l = strlen(progress.payload);
				
				
				for (int i = 0; i < l; i++)
				{
					out_fname[i] = progress.payload[i];
					if (l - i < 6)
					{
						char aux[15] = "_out_cont.json";
						strcat(out_fname,aux);
						break;
					}
				}

				snprintf(cmd, 512, "/home/root/trajectory %s %d -c /home/root/initial_config.json -p 100 -cont %s > last_log.txt &", progress.payload, n,out_fname);
				// printf("%s",cmd);
				system(cmd);
			}
			break;
		case 2:
			// Move joints
			cmd = reinterpret_cast<char *>(malloc(300));
			// Not really progress nor n, don't know how to solve this right now :P
			snprintf(cmd, 300, "/home/root/sendRef %d %d", progress.mode, n);
			system(cmd);
			break;
		case 3:
			// Reset spid (ConfigureInit)
			cmd = reinterpret_cast<char *>(malloc(20));
			snprintf(cmd, 20, "/home/root/reset");
			system(cmd);
			break;
		case 4:
			// Home
			cmd = reinterpret_cast<char *>(malloc(20));
			snprintf(cmd, 20, "/home/root/home");
			system(cmd);
			break;

		default:
			// free(cmd);
			break;
		}
		free(cmd);
	}
}

void parse_command(char *command, int *t, char *m, char *url, int *n)
{

	char *pch;

	pch = strtok(command, "[],");
	int type = atoi(pch);
	*t = type;
	pch = strtok(NULL, "[],");
	char mode = pch[0];
	*m = mode;
	pch = strtok(NULL, "[],");
	// char buf[100];
	strcpy(url, pch);
	pch = strtok(NULL, "[],");
	*n = atoi(pch);
// url = buf;
#ifdef EDS_VERBOSE

	printf("type: %d\n", type);
	printf("mode: %c\n", mode);
	printf("url: %s\n", url);

#endif
}
// esto va en el archivo trajectory.cpp
void *pub_progress(void *buf)
{
	char *payload = (char *)buf;
	int rc = mosquitto_publish(mosq, NULL, "/EDScorbot/trajectory", strlen(payload), payload, 1, false);
	int *p = &rc;
	void *v = (void *)p;
	return v;
}

void ftp_trajectory(char *url)
{

	// descargar trayectoria y ejecutarla
	// system("execute_trajectory ....");
	// pthread_t pub_thread;
}

int main(int argc, char *argv[])
{

	uint8_t reconnect = true;
	char clientid[24];
	int rc = 0;

	signal(SIGINT, handle_signal);
	signal(SIGTERM, handle_signal);

	mosquitto_lib_init();

	memset(clientid, 0, 24);
	snprintf(clientid, 23, "mysql_log_%d", getpid());
	mosq = mosquitto_new(clientid, true, 0);
	progress.last = 0;
	if (mosq)
	{
		// mosquitto_connect_callback_set(mosq, connect_callback);
		mosquitto_message_callback_set(mosq, message_callback);

		rc = mosquitto_connect(mosq, mqtt_host, mqtt_port, 60);

		mosquitto_subscribe(mosq, NULL, "/EDScorbot/commands", 0);

		while (run)
		{
			rc = mosquitto_loop(mosq, -1, 1);
			if (run && rc)
			{
				printf("connection error!\n");
				sleep(10);
				mosquitto_reconnect(mosq);
			}
		}
		mosquitto_destroy(mosq);
	}

	mosquitto_lib_cleanup();

	return rc;
}
