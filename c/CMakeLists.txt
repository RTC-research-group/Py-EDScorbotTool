cmake_minimum_required(VERSION 3.10)
project(edscorbot_runtime)


#find_package(PkgConfig REQUIRED)
#pkg_check_modules(Mosquitto IMPORTED_TARGET libmosquitto REQUIRED)


## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++17)

add_subdirectory("json")
add_subdirectory("src/trajectory")
#set(nlohmann_json_DIR "/home/enrique/Trabajo/Py-EDScorbotTool/c/src/json/cmake")
#find_package(nlohmann_json 3.10.5 REQUIRED)
## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages

SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -fPIC --static  -DEDS_VERBOSE")
SET(CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -DEDS_VERBOSE")

# Custom CMake base module

# Compile this module (standard C++ file, no additional dependencies)
#add_library(test_target SHARED src/testModule.cpp)
add_executable(test_edscorbot src/EDScorbot.cpp src/test_joints.cpp src/devmem.cpp)
add_executable(server src/server.cpp src/EDScorbot.cpp src/devmem.cpp)
add_executable(test_read src/EDScorbot.cpp src/read_joints.cpp src/devmem.cpp)
add_executable(receive_server src/receive_server.cpp)
add_executable(test_json src/test_json.cpp)
add_executable(test_home src/test_home.cpp src/EDScorbot.cpp src/devmem.cpp)
add_executable(reset src/reset_all.cpp src/EDScorbot.cpp src/devmem.cpp)
#add_executable(trajectory src/trajectory.cpp src/EDScorbot.cpp src/devmem.cpp)
add_executable(mqtt_client src/mqtt_client.c)



#add_library(image_generator SHARED src/Image_generator.cpp)


# SET_TARGET_PROPERTIES(test_target
# 	PROPERTIES
# 	SUFFIX ".so"
# )

#target_include_directories(test_target PUBLIC "/usr/include")
target_include_directories(test_edscorbot PUBLIC "c/json/single_include/")
target_include_directories(test_edscorbot PUBLIC "c/src/include")

target_include_directories(test_read PUBLIC "c/json/single_include/")
target_include_directories(test_read PUBLIC "c/src/include")

target_include_directories(test_json PUBLIC "c/json/single_include/")
target_include_directories(test_json PUBLIC "c/src/include")

target_include_directories(test_home PUBLIC "c/json/single_include/")
target_include_directories(test_home PUBLIC "c/src/include")


target_include_directories(reset PUBLIC "c/json/single_include/")
target_include_directories(reset PUBLIC "c/src/include")

target_include_directories(server PUBLIC "c/json/single_include/")
target_include_directories(server PUBLIC "c/src/")

target_include_directories(receive_server PUBLIC "c/json/single_include/")
target_include_directories(receive_server PUBLIC "c/src/")



target_include_directories(mqtt_client PUBLIC "c/json/single_include/")
target_include_directories(mqtt_client PUBLIC "c/src/")
target_include_directories(mqtt_client PUBLIC "/home/enrique/mosquitto-2.0.14/include")


#TARGET_LINK_LIBRARIES(test_target PRIVATE ${DV_LIBRARIES})
TARGET_LINK_LIBRARIES(test_edscorbot PRIVATE nlohmann_json::nlohmann_json)
TARGET_LINK_LIBRARIES(test_read PRIVATE nlohmann_json::nlohmann_json)
TARGET_LINK_LIBRARIES(test_json PRIVATE nlohmann_json::nlohmann_json)

TARGET_LINK_LIBRARIES(test_home PRIVATE nlohmann_json::nlohmann_json)

TARGET_LINK_LIBRARIES(reset PRIVATE nlohmann_json::nlohmann_json)

SET(CMAKE_BUILD_TYPE "Debug")
TARGET_LINK_LIBRARIES(server PRIVATE nlohmann_json::nlohmann_json)
#TARGET_LINK_LIBRARIES(trajectory PRIVATE nlohmann_json::nlohmann_json)
TARGET_LINK_LIBRARIES(mqtt_client /home/enrique/Trabajo/Py-EDScorbotTool/c/compiled_libs_armhf/libmosquitto.a -lpthread)



#target_link_libraries(trajectory PRIVATE PkgConfig::Mosquitto)

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
