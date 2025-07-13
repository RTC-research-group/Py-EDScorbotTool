#!/bin/bash

cd ../
git clone https://github.com/eclipse/mosquitto >> script_log.txt
git clone https://github.com/nlohmann/json/ >> script_log.txt
cd mosquitto >> script_log.txt
rm -rf build >> script_log.txt
mkdir build >> script_log.txt
cd build >> script_log.txt
cmake .. -DWITH_STATIC_LIBRARIES=ON -DWITH_PIC=ON -DWITH_TLS=OFF -DWITH_WEBSOCKETS=ON >> script_log.txt
make -j4 >> script_log.txt

ls -l lib >> script_log.txt
mkdir ../../lib >> script_log.txt
cp lib/libmosquitto_static.a ../../lib >> script_log.txt