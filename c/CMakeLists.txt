cmake_minimum_required(VERSION 3.10)
project(edscorbot_runtime)



#find_package(PkgConfig REQUIRED)
#pkg_check_modules(Mosquitto IMPORTED_TARGET libmosquitto REQUIRED)
# fetch latest argparse
include(FetchContent)
FetchContent_Declare(
    argparse
    GIT_REPOSITORY https://github.com/p-ranav/argparse.git
)
FetchContent_MakeAvailable(argparse)

#execute_process(
#    COMMAND bash "-c" "../mosquitto_build.sh" 
#    OUTPUT_VARIABLE FOO
#)


## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++17)

#add_subdirectory("json")
#add_subdirectory("src/include")
# remove trajectory dolfer due to compilation problems(dependencies)
#add_subdirectory("src/trajectory")
add_subdirectory("src/mqtt_server")
#set(nlohmann_json_DIR "/home/enrique/Trabajo/Py-EDScorbotTool/c/src/json/cmake")
#find_package(nlohmann_json 3.10.5 REQUIRED)
## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages

SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -fPIC --static  -DEDS_VERBOSE")
SET(CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -DEDS_VERBOSE")
SET(HEADER_FILES src/include/EDScorbot.hpp)
#cmake_path(SET project_base_dir ..)
#message("Directorios: ${CMAKE_BINARY_DIR}\t${CMAKE_SOURCE_DIR}\t${CMAKE_CURRENT_BINARY_DIR}\t${CMAKE_CURRENT_SOURCE_DIR}")
#message("DIRECTORIO BASE PROYECTO: ${project_base_dir}")
# Custom CMake base module

# Compile this module (standard C++ file, no additional dependencies)
#add_library(test_target SHARED src/testModule.cpp)
#add_executable(test_edscorbot src/EDScorbot.cpp src/test_joints.cpp src/devmem.cpp)
#add_executable(server src/server.cpp src/EDScorbot.cpp src/devmem.cpp)
add_executable(read_joints src/EDScorbot/EDScorbot.cpp src/scripts/read_joints.cpp src/EDScorbot/devmem.cpp ${HEADER_FILES})
add_executable(test_arrays src/test_scripts/test_arrays.cpp)
add_executable(test_argparse src/test_scripts/test_argparse.cpp)
add_executable(test_putenv src/test_scripts/test_putenv.cpp)

# add_executable(receive_server src/receive_server.cpp)
add_executable(test_json src/test_scripts/test_json.cpp)
add_executable(home src/scripts/home.cpp src/EDScorbot/EDScorbot.cpp src/EDScorbot/devmem.cpp ${HEADER_FILES})
add_executable(reset src/scripts/reset_all.cpp src/EDScorbot/EDScorbot.cpp src/EDScorbot/devmem.cpp ${HEADER_FILES})
add_executable(send_home src/scripts/send_0.cpp src/EDScorbot/EDScorbot.cpp src/EDScorbot/devmem.cpp ${HEADER_FILES})
add_executable(sendRef src/scripts/sendRefJx.cpp src/EDScorbot/EDScorbot.cpp src/EDScorbot/devmem.cpp ${HEADER_FILES})

#add_executable(trajectory src/trajectory.cpp src/EDScorbot.cpp src/devmem.cpp)
# add_executable(mqtt_client src/mqtt_client.c)

#executable for mocked server
add_executable(mocked_server src/mqtt_server/mocked_server.cpp src/EDScorbot/devmem.cpp)

#executable for conversion tests of objects, json and strings (new model)

add_executable(tests_json_objects src/test_scripts/test_json_objects.cpp)


#add_library(image_generator SHARED src/Image_generator.cpp)


# SET_TARGET_PROPERTIES(test_target
# 	PROPERTIES
# 	SUFFIX ".so"
# )

#target_include_directories(test_target PUBLIC "/usr/include")
# target_include_directories(test_edscorbot PUBLIC "c/json/single_include/")
# target_include_directories(test_edscorbot PUBLIC "c/src/include")

#message("My test's working directory: ${PROJECT_SOURCE_DIR}")
# target_include_directories(read_joints PUBLIC "c/json/single_include/")
target_include_directories(read_joints PUBLIC "src")

# target_include_directories(test_json PUBLIC "c/json/single_include/")
target_include_directories(test_json PUBLIC "src")

# target_include_directories(home PUBLIC "c/json/single_include/")
target_include_directories(home PUBLIC "src" "./" "${CMAKE_CURRENT_SOURCE_DIR}/json/single_include/")


# target_include_directories(reset PUBLIC "c/json/single_include/")
target_include_directories(reset PUBLIC "src" "./")
target_include_directories(send_home PUBLIC "src" "./")

target_include_directories(test_argparse PUBLIC "src" "./")
target_include_directories(test_putenv PUBLIC "src" "./")

#target_include_directories(sendRef PUBLIC "src" "./" "${CMAKE_CURRENT_SOURCE_DIR}/json/single_include/")
target_include_directories(sendRef PUBLIC "src" "./")

target_include_directories(mocked_server PUBLIC "src" "${CMAKE_CURRENT_SOURCE_DIR}/json/single_include/")
target_include_directories(tests_json_objects PUBLIC "src" "${CMAKE_CURRENT_SOURCE_DIR}/json/single_include/")

 #TARGET_LINK_LIBRARIES(mocked_server PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/compiled_libs_x86/libmosquitto_static.a" -lpthread )
TARGET_LINK_LIBRARIES(mocked_server PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/compiled_libs_armhf/libmosquitto.a" -lpthread )


#target_include_directories(reset PUBLIC "c/src/include")


# target_include_directories(server PUBLIC "c/json/single_include/")
# target_include_directories(server PUBLIC "c/src/")

# target_include_directories(receive_server PUBLIC "c/json/single_include/")
# target_include_directories(receive_server PUBLIC "c/src/")



# target_include_directories(mqtt_client PUBLIC "c/json/single_include/")
# target_include_directories(mqtt_client PUBLIC "c/src/")
# target_include_directories(mqtt_client PUBLIC "/home/enrique/mosquitto-2.0.14/include")


#TARGET_LINK_LIBRARIES(test_target PRIVATE ${DV_LIBRARIES})
# TARGET_LINK_LIBRARIES(test_edscorbot PRIVATE nlohmann_json::nlohmann_json)

## commented because nlohmann lib has been compiled and installed with make install
#TARGET_LINK_LIBRARIES(read_joints PRIVATE nlohmann_json::nlohmann_json)
#TARGET_LINK_LIBRARIES(test_json PRIVATE nlohmann_json::nlohmann_json)

#TARGET_LINK_LIBRARIES(home PRIVATE nlohmann_json::nlohmann_json)

#TARGET_LINK_LIBRARIES(reset PRIVATE nlohmann_json::nlohmann_json)
#TARGET_LINK_LIBRARIES(send_home PRIVATE nlohmann_json::nlohmann_json)

#TARGET_LINK_LIBRARIES(test_argparse PUBLIC argparse)
#TARGET_LINK_LIBRARIES(test_argparse PRIVATE argparse nlohmann_json::nlohmann_json)



SET(CMAKE_BUILD_TYPE "Debug")
# TARGET_LINK_LIBRARIES(server PRIVATE nlohmann_json::nlohmann_json)
#TARGET_LINK_LIBRARIES(trajectory PRIVATE nlohmann_json::nlohmann_json)
# TARGET_LINK_LIBRARIES(mqtt_client /home/enrique/Trabajo/Py-EDScorbotTool/c/compiled_libs_armhf/libmosquitto.a -lpthread)



#target_link_libraries(trajectory PRIVATE PkgConfig::Mosquitto)

#INSTALL(TARGETS test_edscorbot DESTINATION "/usr/share/dv/modules")
#INSTALL(TARGETS image_generator DESTINATION "/usr/share/dv/modules")

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)
# SET(CMAKE_BUILD_TYPE "Debug")


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
