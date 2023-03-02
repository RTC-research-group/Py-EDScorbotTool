#!/bin/bash

cd ../mosquitto
rm -rf build
mkdir build
cd build
cmake .. -DWITH_STATIC_LIBRARIES=ON -DWITH_PIC=ON -DWITH_TLS=OFF
make -j4

ls -l lib
mkdir ../../lib
cp lib/libmosquitto_static.a ../../lib