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

    char *filename = argv[1];
    int n = atoi(argv[2]);
    std::ifstream arr_stream(filename, std::ios::in);
    json js = json::parse(arr_stream);


    int initial_position[6]={js["Joint_initial_positions"]["J1"],js["Joint_initial_positions"]["J2"],js["Joint_initial_positions"]["J3"],js["Joint_initial_positions"]["J4"],js["Joint_initial_positions"]["J5"],js["Joint_initial_positions"]["J6"]};
    
    char traj_index[5];
    snprintf(traj_index,5,"#%d",n);
    json trajectory = js["Trajectories"][traj_index];
    int n_steps = trajectory["steps"];
    
    int *pjx[6];
    for (int i = 0; i < 6; i++)
    {
        pjx[i] = reinterpret_cast<int *>(malloc(sizeof(int) * n_steps));
        printf("%d\n",initial_position[i]);
    }

    auto tj1 = trajectory["J1"];
    
    std::cout << tj1 << "tj1" << std::endl;
    for (int i = 0; i< 10; i++){
        printf("%d\n",(int)tj1[i]);
    }
    // for(int i = 0;i < trajectory["J1"].size();i++){
        
    //     std::cout << trajectory["J1"] << 
    // }
    for (int i = 0; i < 6; i++)
    {
        free(pjx[i]);
        
    }

    // float j1[500], j2[500];
    // float *pjx[6];
    // for (int i = 0; i < 6; i++)
    // {
    //     pjx[i] = reinterpret_cast<float *>(malloc(sizeof(float) *500));
    // }

    // // float j1[500], j2[500];
    // // parse_jsonnp_array(argv[1], &j1[0], &j2[0], &j3[0], &j4[0], &j5[0], &j6[0]);
    // parse_jsonnp_array(argv[1], pjx[0], pjx[1], pjx[2], pjx[3], pjx[4], pjx[5]);
    // parse_jsonnp_array(argv[1], &j1[0], &j2[0], &j3[0], &j4[0], &j5[0], &j6[0]);

    // printf("%f,%f\n", j1[0], j2[0]);
    //   float j1_angles[500], j2_angles[500];
    //   w_to_angles(j1_angles,j2_angles,j1,j2);
    // for(int i = 0; i< 500;i++){
    //     printf("i: %d\t[%f,%f,%f,%f,%f,%f]\n",i,pjx[0][i],pjx[1][i],pjx[2][i],pjx[3][i],pjx[4][i],pjx[5][i]);
    // }
    // json js;
    // for (int i = 0; i < 500; i++)
    // {
    //     // Construir el json aqui
    //     js[i] = {pjx[0][i],pjx[1][i],pjx[2][i],pjx[3][i],pjx[4][i],pjx[5][i], 150};
    // }
    // std::ofstream o("test_json_write.json");
    // o << std::setw(4) << js << std::endl; // Conversion y envío de resultados en json
    // o.close();
    // for(int i = 0; i<6;i++){
    //     free(pjx[i]);
    // }
    return 0;
}

<<<<<<< HEAD
void parse_jsonnp_array(char *filename, float *j1, float *j2)
=======
void parse_jsonnp_array(char *filename, float *j1, float *j2, float *j3, float *j4, float *j5, float *j6)
>>>>>>> origin/dev
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

<<<<<<< HEAD
void w_to_angles(float *j1_angles, float *j2_angles, float *j1, float *j2)
=======
void w_to_angles(int n, float *j1_angles, float *j2_angles, float *j3_angles, float *j4_angles, float *j5_angles, float *j6_angles,
                 float *j1, float *j2, float *j3, float *j4, float *j5, float *j6)
>>>>>>> origin/dev
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
<<<<<<< HEAD
        #ifdef DEBUG
        printf("[%f\t%f ]\n", j1_angles[i], j2_angles[i]);
        #endif
=======
        j3_angles[i] = (j3[i] * (0.001) * (180 / PI)) + j3_angles[i - 1];
        j4_angles[i] = (j4[i] * (0.001) * (180 / PI)) + j4_angles[i - 1];
        j5_angles[i] = (j5[i] * (0.001) * (180 / PI)) + j5_angles[i - 1];
        j6_angles[i] = (j6[i] * (0.001) * (180 / PI)) + j6_angles[i - 1];
#ifdef DEBUG
        printf("[%f\t%f\t%f%f\t%f\t%f]\n", j1_angles[i], j2_angles[i], j3_angles[i], j4_angles[i], j5_angles[i], j6_angles[i]);
#endif
>>>>>>> origin/dev
    }
}
