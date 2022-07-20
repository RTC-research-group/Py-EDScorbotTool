#include "nlohmann/json.hpp"
#include <map>
#include <iostream>
#include <fstream>
#include <vector>
#include "include/EDScorbot.hpp"
#define PI 3.141592653589793
using json = nlohmann::json;
#define SLEEP 0.25

// Function to parse numpy array in json format
void parse_jsonnp_array(char *filename, float *j1, float *j2);

// Function to transform a trajectory from angular velocities (w, omega) to angles
void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2);

int main(int argc, char *argv[])
{
    // argv[1] --> datos en json

    float j1[500], j2[500];
    parse_jsonnp_array(argv[1], j1, j2);
    // printf("%f,%f\n", j1[0], j2[0]);
    float j1_angles[500], j2_angles[500];
    w_to_angles(j1_angles, j2_angles, j1, j2);

    // Inicializacion scorbot
    // argv[2] --> initial_config.json
    char *config_file = argv[2];
    EDScorbot handler(config_file);
    
    std::vector<int> j1_vector,j2_vector;
    int j1_pos[500],j2_pos[500];

    handler.initJoints();
    int i;
    for (i = 0; i < 500; i++)
    {
        int refj1, refj2;
        refj1 = handler.angle_to_ref(1,j1_angles[i]);
        refj2 = handler.angle_to_ref(2,j2_angles[i]);
        printf("It: %d, J1: %d, J2: %d\n",i,refj1,refj2);
        //handler.sendRef(refj1, handler.j1);
        //handler.sendRef(refj2, handler.j2);
        clock_t start = clock();
        clock_t end = clock();
        float elapsed = (end-start)/CLOCKS_PER_SEC;
        while (elapsed < SLEEP)
        {
            /*Do something*/
            end = clock();
            elapsed = (end-start)/CLOCKS_PER_SEC;
            int joints[6];
            handler.readJoints(joints);
            j1_vector.push_back(joints[0]);
            j2_vector.push_back(joints[1]);

        }
        j1_pos[i]=j1_vector.back();
        j2_pos[i]=j2_vector.back();
    }

    for (i = 0; i < 500; i++){
        printf("i: %d, j1: %d, j2: %d\n",i,j1_pos[i],j2_pos[i]);

    }

    for (int e:j1_vector){
        std::cout <<' ' <<e << ' ';
    }
    std::cout << std::endl;
    
    for (int e:j2_vector){
        std::cout <<' ' <<e << ' ';
    }
    std::cout << std::endl;
    // Ejecucion de la trayectoria con j1 y j2

    // Recogida de resultados? Listas de c++ o arrays de c?

    // Conversion y envío de resultados en json
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
