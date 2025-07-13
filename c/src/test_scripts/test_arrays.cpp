#include <iostream>
#include <vector>
#include <iterator>
#include <algorithm>
#include <cstdlib>
#include <tuple>
#include <fstream> // looks like we need this too (edit by π)
#include <stdlib.h>
#include <cstring>
#define str std::string

void write_vector_to_file(std::vector<int> v, std::string filename)
{//FUNCIONA!!!!

    FILE *f;
    f = fopen(filename.c_str(),"wb");

    fwrite(&v[0],sizeof(int),v.size(),f);
    //std::memcpy(&v[0],f,);
    fclose(f);
    
}   

int read_vector_from_file(int* v, int size, std::string filename)
{
    //FUNCIONA!!!!
    FILE *f;
    f = fopen(filename.c_str(),"rb");
    fread(v,sizeof(int),size,f);
    fclose(f);
    return 0;
}

void write_tuple_vector_to_files(std::vector<std::tuple<int, int, int, int, int, int, int>> v, std::string fname_base)
{
    std::vector<int> vj1, vj2, vj3, vj4, vj5, vj6, vts;
    
    std::string f1, f2, f3, f4, f5, f6,fts;
    f1 = fname_base + "_j1";
    f2 = fname_base + "_j2";
    f3 = fname_base + "_j3";
    f4 = fname_base + "_j4";
    f5 = fname_base + "_j5";
    f6 = fname_base + "_j6";
    fts = fname_base + "_ts";

    for (int i = 0; i < v.size(); i++)
    {
        


        vj1.push_back(std::get<0>(v[i]));
        vj2.push_back(std::get<1>(v[i]));
        vj3.push_back(std::get<2>(v[i]));
        vj4.push_back(std::get<3>(v[i]));
        vj5.push_back(std::get<4>(v[i]));
        vj6.push_back(std::get<5>(v[i]));
        vts.push_back(std::get<6>(v[i]));
    }

    f1 = f1 + "_n" + std::to_string(vj1.size());
    f2 = f2 + "_n" + std::to_string(vj1.size());
    f3 = f3 + "_n" + std::to_string(vj1.size());
    f4 = f4 + "_n" + std::to_string(vj1.size());
    f5 = f5 + "_n" + std::to_string(vj1.size());
    f6 = f6 + "_n" + std::to_string(vj1.size());
    fts = fts + "_n" + std::to_string(vj1.size());
    write_vector_to_file(vj1,f1);
    write_vector_to_file(vj2,f2);
    write_vector_to_file(vj3,f3);
    write_vector_to_file(vj4,f4);
    write_vector_to_file(vj5,f5);
    write_vector_to_file(vj6,f6);
    write_vector_to_file(vts,fts);

    
}

int main()
{
    std::vector<std::tuple<int, int, int, int, int, int, int>> big_v;
    for (int i = 0; i < 500; i++)
    {
        big_v.push_back(std::make_tuple(1, 2, 3, 4, 5, 6, 7));
    }
    std::string filename = str("big_vector");
    //write_vector_to_file(big_v, filename);
    //auto newVector{read_vector_from_file(filename)};
    write_tuple_vector_to_files(big_v,std::string("big_vector"));
    
    int *pj1,*pj2,*pj3,*pj4,*pj5,*pj6,*pts;
    int size = sizeof(int)*big_v.size();
    pj1 = reinterpret_cast<int*>(malloc(size));
    pj2 = reinterpret_cast<int*>(malloc(size));
    pj3 = reinterpret_cast<int*>(malloc(size));
    pj4 = reinterpret_cast<int*>(malloc(size));
    pj5 = reinterpret_cast<int*>(malloc(size));
    pj6 = reinterpret_cast<int*>(malloc(size));
    pts = reinterpret_cast<int*>(malloc(size));
    
    // read_vector_from_file(pj1,vj1.size(),f1);
    // read_vector_from_file(pj2,vj2.size(),f2);
    // read_vector_from_file(pj3,vj2.size(),f3);
    // read_vector_from_file(pj4,vj2.size(),f4);
    // read_vector_from_file(pj5,vj2.size(),f5);
    // read_vector_from_file(pj6,vj2.size(),f6);
    // read_vector_from_file(pts,vj2.size(),fts);
    
    int a = 1;
    free(pj1);
    free(pj2);
    free(pj3);
    free(pj4);
    free(pj5);
    free(pj6);
    free(pts);
    return 0;
}