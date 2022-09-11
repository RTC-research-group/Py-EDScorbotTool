#include <signal.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
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

void parse_command(char *command, int *t, char *m, char *url);
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

		int type;
		char mode;
		char url[100];
		parse_command((char *)message->payload, &type, &mode, url);
		progress.type = type;
		progress.mode = mode;
		progress.payload = url;
		progress.last = 1;
		system("/home/root/trajectory /home/root/test.json /home/root/initial_config.json &");
	}
}

void parse_command(char *command, int *t, char *m, char *url)
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
// url = buf;
#ifdef EDS_VERBOSE

	printf("type: %d\n", type);
	printf("mode: %c\n", mode);
	printf("url: %s\n", url);

#endif
}
//esto va en el archivo trajectory.cpp
void *pub_progress(void *buf)
{
	char *payload = (char *)buf;
	int rc = mosquitto_publish(mosq, NULL, "/EDScorbot/trajectory", strlen(payload), payload, 0, false);
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
