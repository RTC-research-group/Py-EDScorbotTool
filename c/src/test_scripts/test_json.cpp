#include "nlohmann/json.hpp"
#include <map>
#include <iostream>
#include <fstream>
#define PI 3.141592653589793
using json = nlohmann::json;

void parse_jsonnp_array(char *filename, float *j1, float *j2, float *j3, float *j4, float *j5, float *j6);
void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2);
int main(int argc, char *argv[])
{
    int a[10];
    for (int i = 0; i< 10;i++){
        a[i] = rand();
    }
   json js1,js2,js3,js4,js5,js6,jstimestamp;

    for (int i = 0; i < 10; i++)
    {
        // Construir el json aqui
        //js[i] = {state_vector[i].j1, state_vector[i].j2, state_vector[i].j3, state_vector[i].j4, state_vector[i].j5, state_vector[i].j6, state_vector[i].timestamp};
        js1[i] = a[i];
        js2[i] = a[i];
        js3[i] = a[i];
        js4[i] = a[i];
        js5[i] = a[i];
        js6[i] = a[i];
        jstimestamp[i] = a[i];

    }
    json js;
    js["J1"] = js1;
    js["J2"] = js2;
    js["J3"] = js3;
    js["J4"] = js4;
    js["J5"] = js5;
    js["J6"] = js6;
    std::ofstream o("test_json_write.json");
    o << std::setw(4) << js << std::endl; // Conversion y envío de resultados en json
    o.close();
    
    return 0;
    
}

void parse_jsonnp_array(char *filename, float *j1, float *j2, float *j3, float *j4, float *j5, float *j6)
{
    //New format
    //
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

void w_to_angles(int n, float *j1_angles, float *j2_angles, float *j3_angles, float *j4_angles, float *j5_angles, float *j6_angles,
                 float *j1, float *j2, float *j3, float *j4, float *j5, float *j6)
{
    j1_angles[0] = (j1[0] * 0.001) * (180 / PI);
    j2_angles[0] = (j2[0] * 0.001) * (180 / PI);
    j3_angles[0] = (j3[0] * 0.001) * (180 / PI);
    j4_angles[0] = (j4[0] * 0.001) * (180 / PI);
    j5_angles[0] = (j5[0] * 0.001) * (180 / PI);
    j6_angles[0] = (j6[0] * 0.001) * (180 / PI);
    int i = 0;
#ifdef DEBUG
    printf("[%f\t%f ]\n", j1_angles[i], j2_angles[i]);
#endif

    for (i = 1; i < n; i++)
    {
        // np.cumsum(omegas * 0.001,axis=0)*( 180 / np.pi)
        j1_angles[i] = (j1[i] * (0.001) * (180 / PI)) + j1_angles[i - 1];
        j2_angles[i] = (j2[i] * (0.001) * (180 / PI)) + j2_angles[i - 1];
        j3_angles[i] = (j3[i] * (0.001) * (180 / PI)) + j3_angles[i - 1];
        j4_angles[i] = (j4[i] * (0.001) * (180 / PI)) + j4_angles[i - 1];
        j5_angles[i] = (j5[i] * (0.001) * (180 / PI)) + j5_angles[i - 1];
        j6_angles[i] = (j6[i] * (0.001) * (180 / PI)) + j6_angles[i - 1];
#ifdef DEBUG
        printf("[%f\t%f\t%f%f\t%f\t%f]\n", j1_angles[i], j2_angles[i], j3_angles[i], j4_angles[i], j5_angles[i], j6_angles[i]);
#endif
    }
}
