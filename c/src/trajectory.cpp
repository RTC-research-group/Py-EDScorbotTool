#include "nlohmann/json.hpp"
#include <map>
#include <iostream>
#include <fstream>
#define PI 3.141592653589793
using json = nlohmann::json;

void parse_jsonnp_array(char *filename, float *j1, float *j2);
void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2);
int main(int argc, char *argv[])
{
    float j1[500], j2[500];
    parse_jsonnp_array(argv[1], j1, j2);
    // printf("%f,%f\n", j1[0], j2[0]);
    float j1_angles[500], j2_angles[500];
    w_to_angles(j1_angles,j2_angles,j1,j2);

    //Inicializacion scorbot
    char* config_file = argv[2];
    EDScorbot handler(config_file);



    //Ejecucion de la trayectoria con j1 y j2

    //Recogida de resultados? Listas de c++ o arrays de c?

    //Conversion y envío de resultados en json
    return 0;
}

void parse_jsonnp_array(char *filename, float *j1, float *j2)
{
    std::ifstream arr_stream(filename, std::ios::in);
    json array = json::parse(arr_stream);

    for (const auto &[k, v] : array.items())
    {
        int i = atoi(k.c_str());
        j1[i] = v[0];
        j2[i] = v[1];
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
