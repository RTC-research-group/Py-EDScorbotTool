#include "utils.h"
using json = nlohmann::json;

void parse_jsonnp_array(const char *filename, int *j1, int *j2,int *j3, int *j4,int *j5, int *j6)
{
    std::ifstream arr_stream(filename, std::ios::in);
    json array = json::parse(arr_stream);

    for (const auto &[k, v] : array.items())
    {
        int i = atoi(k.c_str());
        j1[i] = v[0];
        j2[i] = v[1];
        j3[i] = v[2];
        j4[i] = v[3];
        j5[i] = v[4];
        j6[i] = v[5];
        // std::cout << "Key: " << k << std::endl;
        // std::cout << "Value: " << v[1] << std::endl;
    }
    return;
}

void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2)
{
    j1_angles[0] = (j1[0] * 0.001) * (180 / PI);
    j2_angles[0] = (j2[0] * 0.001) * (180 / PI);
    int i = 0;
#ifdef DEBUG
    printf("[%f\t%f ]\n", j1_angles[i], j2_angles[i]);
#endif

    for (i = 1; i < 500; i++)
    {
        // np.cumsum(omegas * 0.001,axis=0)*( 180 / np.pi)
        j1_angles[i] = (j1[i] * (0.001) * (180 / PI)) + j1_angles[i - 1];
        j2_angles[i] = (j2[i] * (0.001) * (180 / PI)) + j2_angles[i - 1];
#ifdef DEBUG
        printf("[%f\t%f ]\n", j1_angles[i], j2_angles[i]);
#endif
    }
}

void init_mqtt_client(mosquitto *mosq, const char *broker_ip)
{
    int rc;

    rc = mosquitto_connect(mosq, broker_ip, 1883, 60);
    while (rc != 0)
    {
        printf("Client could not connect to broker! Error Code: %d\nTrying to reconnect...\n", rc);
        rc = mosquitto_connect(mosq, broker_ip, 1883, 60);

        // mosquitto_destroy(mosq);
        // return -1;
    }
    printf("We are now connected to the broker!\n");

    // SUBSCRIBE!
}

int publish(mosquitto *mosq, char *msg, int msg_len, const char *topic)
{
    int ret = mosquitto_publish(mosq, NULL, topic, msg_len, msg, 0, false);
    return ret;
}

void end_mqtt_client(mosquitto *mosq)
{
    mosquitto_disconnect(mosq);
    mosquitto_destroy(mosq);

    mosquitto_lib_cleanup();
}

long int time_in_micros(timeval t)
{
    long int time_in_microseconds = ((t.tv_sec * 1000000) + t.tv_usec);
    return time_in_microseconds;
}

void write_vector_to_file(std::vector<int> v, std::string filename)
{//FUNCIONA!!!!

    FILE *f;
    f = fopen(filename.c_str(),"wb");

    fwrite(&v[0],sizeof(int),v.size(),f);
    //std::memcpy(&v[0],f,);
    fclose(f);
    
}   

int read_vector_from_file(int* v, int n, std::string filename)
{
    //FUNCIONA!!!!
    FILE *f;
    f = fopen(filename.c_str(),"rb");
    fread(v,sizeof(int),n,f);
    fclose(f);
    return 0;
}
