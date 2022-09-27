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
    // float j1[500], j2[500];
    float *pjx[6];
    for (int i = 0; i < 6; i++)
    {
        pjx[i] = reinterpret_cast<float *>(malloc(sizeof(float) *500));
    }

    // float j1[500], j2[500];
    // parse_jsonnp_array(argv[1], &j1[0], &j2[0], &j3[0], &j4[0], &j5[0], &j6[0]);
    parse_jsonnp_array(argv[1], pjx[0], pjx[1], pjx[2], pjx[3], pjx[4], pjx[5]);
    // parse_jsonnp_array(argv[1], &j1[0], &j2[0], &j3[0], &j4[0], &j5[0], &j6[0]);

    // printf("%f,%f\n", j1[0], j2[0]);
    //   float j1_angles[500], j2_angles[500];
    //   w_to_angles(j1_angles,j2_angles,j1,j2);
    for(int i = 0; i< 500;i++){
        printf("i: %d\t[%f,%f,%f,%f,%f,%f]\n",i,pjx[0][i],pjx[1][i],pjx[2][i],pjx[3][i],pjx[4][i],pjx[5][i]);
    }
    json js;
    for (int i = 0; i < 500; i++)
    {
        // Construir el json aqui
        js[i] = {pjx[0][i],pjx[1][i],pjx[2][i],pjx[3][i],pjx[4][i],pjx[5][i], 150};
    }
    std::ofstream o("test_json_write.json");
    o << std::setw(4) << js << std::endl; // Conversion y envío de resultados en json
    o.close();
    for(int i = 0; i<6;i++){
        free(pjx[i]);
    }
    return 0;
    
}

void parse_jsonnp_array(char *filename, float *j1, float *j2, float *j3, float *j4, float *j5, float *j6)
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
