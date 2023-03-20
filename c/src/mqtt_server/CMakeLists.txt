cmake_minimum_required(VERSION 3.10)
project(edscorbot_runtime)


find_package(PkgConfig REQUIRED)
pkg_check_modules(Mosquitto IMPORTED_TARGET libmosquitto REQUIRED)


## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++17)

#set(nlohmann_json_DIR "/home/enrique/Trabajo/Py-EDScorbotTool/c/src/json/cmake")
#find_package(nlohmann_json 3.10.5 REQUIRED)
## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS_INIT}")
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -fPIC -DEDS_VERBOSE")
set(LANGUAGE C_STANDARD)
# Custom CMake base module

# Compile this module (standard C++ file, no additional dependencies)
#add_library(test_target SHARED src/testModule.cpp)

add_executable(mqtt_server mqtt_server.cpp ../EDScorbot/EDScorbot.cpp ../EDScorbot/devmem.cpp)
#add_executable(mqtt_client src/mqtt_client.c)




#add_library(image_generator SHARED src/Image_generator.cpp)


# SET_TARGET_PROPERTIES(test_target
# 	PROPERTIES
# 	SUFFIX ".so"
# )



target_include_directories(mqtt_server PUBLIC "../../json/single_include/")
target_include_directories(mqtt_server PUBLIC "../")
#target_include_directories(mqtt_server PUBLIC "/home/enrique/mosquitto-2.0.14/include")
target_include_directories(mqtt_server PUBLIC "../../mosquitto/include")

#TARGET_LINK_LIBRARIES(test_target PRIVATE ${DV_LIBRARIES})
#message("###########DIRECTORIO###########3: ${CMAKE_CURRENT_SOURCE_DIR}")
TARGET_LINK_LIBRARIES(mqtt_server PRIVATE nlohmann_json::nlohmann_json ${CMAKE_CURRENT_SOURCE_DIR}/../../lib/libmosquitto_static.a -lpthread)

#TARGET_LINK_LIBRARIES(mqtt_server )

#INSTALL(TARGETS test_edscorbot DESTINATION "/usr/share/dv/modules")
#INSTALL(TARGETS image_generator DESTINATION "/usr/share/dv/modules")

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)
SET(CMAKE_BUILD_TYPE "Debug")


#target_include_directories(caller PUBLIC "/home/ubuntu/libs/ros_lib/")
#target_include_directories(caller PUBLIC "/home/ubuntu/ros_app/src/movement/include")
#include_directories("/home/ubuntu/customapp/src/helloros/src/")
#add_executable(movement src/spinning.cpp)



#add_library(movclas src/RosConnection.cpp)

#add_executable(helloros src/helloro.cpp)
#target_sources(movement src/movement.cpp)
#target_link_libraries(helloros ${catkin_LIBRARIES})
#target_link_libraries(helloros -lpthread)
#target_link_libraries(movement movlib)
#target_link_libraries(movement ${catkin_LIBRARIES})
#target_link_libraries(movement -lpthread)
#target_link_libraries(movclas movlib)
#target_link_libraries(example movclas)

#target_link_libraries(example PUBLIC movclass)
#target_link_libraries(example PUBLIC ${catkin_LIBRARIES})
#target_link_libraries(example PUBLIC -lpthread)

