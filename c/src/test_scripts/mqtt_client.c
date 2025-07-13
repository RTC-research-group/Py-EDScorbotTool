#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "mosquitto.h"

int main()
{
	int rc;
	struct mosquitto *mosq;

	mosquitto_lib_init();

	mosq = mosquitto_new("publisher-test", true, NULL);

	rc = mosquitto_connect(mosq, "192.168.1.104", 1883, 60);
	if (rc != 0)
	{
		printf("Client could not connect to broker! Error Code: %d\n", rc);
		mosquitto_destroy(mosq);
		return -1;
	}
	printf("We are now connected to the broker!\n");
	for (int i = 0; i < 500; i++)
	{
		
		char buf[100];

		snprintf(buf, 100, "[1,2,3,4,5,6,%d]", i);
		printf("%s\n", buf);
		mosquitto_publish(mosq, NULL, "EDScorbot/trajectory", strlen(buf), buf, 1, false);
		usleep(10000);
	}
	// mosquitto_publish(mosq, NULL, "test/t1", 6, "Hello", 0, false);

	mosquitto_disconnect(mosq);
	mosquitto_destroy(mosq);

	mosquitto_lib_cleanup();
	return 0;
}
