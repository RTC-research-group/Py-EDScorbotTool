#include "include/EDScorbot.hpp"

int main()
{
   
    EDScorbot handler("../initial_config.json");
    handler.sendRef(50,handler.j1);
    return 0;

}