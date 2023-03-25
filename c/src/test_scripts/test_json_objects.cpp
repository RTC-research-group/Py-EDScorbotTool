#include "nlohmann/json.hpp"
#include <assert.h>
#include <string>
#include <iostream>
#include "../impl/server-impls.cpp" 

using json = nlohmann::json;



void test_client_to_str(Client c,std::string expected){
    //printf("testing conversion from client to str\n");
    std::cout << std::endl << "Testing conversion from client to str" << std::endl;
    std::cout << "Client " << c.id << " to str: " << c.to_json().dump();
    assert(strcmp(c.to_json().dump().c_str(),expected.c_str()) == 0);
    std::cout << " (PASSED)" << std::endl;
}

void test_str_to_client(std::string json_str, Client expected){
    std::cout << std::endl << "Testing conversion from str to Client" << std::endl;
    std::cout << "String " << json_str ;
    assert( Client::from_json_string(json_str) == expected);
    std::cout << " (PASSED)" << std::endl;
}

void test_client_is_valid(Client client){
    bool valid = client.is_valid();
    printf("PASSED");
}

void test_client(){
    Client mockedClient = Client();
    mockedClient.id = "adalberto.cajueiro@gmail.com";
    test_client_to_str(mockedClient, mockedClient.to_json().dump());
    test_str_to_client(mockedClient.to_json().dump(),mockedClient);
    test_client_is_valid(mockedClient);
}

void test_metainfo_to_str(MetaInfoObject c){
    std::cout << std::endl << "Testing conversion from metainfo to str" << std::endl;
    std::cout << "MetaInfo: " << c.to_json().dump() ;
    
    std::cout << " (PASSED)" << std::endl;
}

void test_str_to_metainfo(std::string json_str,MetaInfoObject expected){
    std::cout << std::endl << "Testing conversion from str to metainfo" << std::endl;
    std::cout << "String: " << json_str << std::endl;
    assert(MetaInfoObject::from_json_string(json_str) == expected);
    std::cout << " (PASSED)" << std::endl;
}

void test_metainfo(){
    MetaInfoObject mi = initial_metainfoobj();
    test_metainfo_to_str(mi);
    test_str_to_metainfo(mi.to_json().dump(), mi);
}

void test_commandobject_to_str(CommandObject c){
    std::cout << std::endl << "Testing conversion from commandobj to str" << std::endl;
    std::cout << "CommandObj: " << c.to_json().dump() ;
    
    std::cout << " (PASSED)" << std::endl;
}

void test_str_to_commandobj(std::string json_str,CommandObject expected){
    std::cout << std::endl << "Testing conversion from str to commandobj" << std::endl;
    std::cout << "String: " << json_str << std::endl;
    assert(CommandObject::from_json_string(json_str) == expected);
    std::cout << " (PASSED)" << std::endl;
}

void test_commandobj(){
    Point p = Point({1,1,1,1,1,1});
    CommandObject comm = CommandObject(ARM_CONNECT,p);
    comm.client.id = "adalberto.comm@gmail.com";

    Trajectory t = Trajectory(
        std::list<Point>(
            {
                Point({1,1,1,1,1,1}),
                Point({2,2,2,2,2,2}),
                Point({3,3,3,3,3,3}),
                Point({4,4,4,4,4,4})
            }
        )
    );
    CommandObject comm2 = CommandObject(ARM_APPLY_TRAJECTORY,t);
    comm2.client.id = "adalberto.comm2@gmail.com";

    test_commandobject_to_str(comm);
    test_str_to_commandobj(comm.to_json().dump().c_str(),comm);

    test_commandobject_to_str(comm2);
    test_str_to_commandobj(comm2.to_json().dump().c_str(),comm2);
}


void test_movedobj_to_str(MovedObject c){
    std::cout << std::endl << "Testing conversion from movedobj to str" << std::endl;
    std::cout << "Movedobj: " << c.to_json().dump() ;
    
    std::cout << " (PASSED)" << std::endl;
}

void test_str_to_movedobj(std::string json_str,MovedObject expected){
    std::cout << std::endl << "Testing conversion from str to movedObj" << std::endl;
    std::cout << "String: " << json_str << std::endl;
    assert( MovedObject::from_json_string(json_str) == expected);
    std::cout << " (PASSED)" << std::endl;
}

void test_movedobj(){
    MovedObject m = MovedObject();
    m.client = Client("adalberto");
    m.error = false;
    m.content = Point({1,2,3,4});

    test_movedobj_to_str(m);
    test_str_to_movedobj(m.to_json().dump(), m);
}

int main(int argc, char *argv[])
{
    std::cout << "Starting tests" << std::endl;
    test_client();
    test_metainfo();
    test_commandobj();
    test_movedobj();
}
