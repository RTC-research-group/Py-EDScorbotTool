#!/bin/sh

./test_edscorbot 1 100 1 ./initial_config.json
./test_edscorbot 2 100 0 ./initial_config.json
./test_edscorbot 3 100 0 ./initial_config.json
./test_edscorbot 4 100 0 ./initial_config.json
./test_edscorbot 5 100 0 ./initial_config.json

sleep 0.001

./test_edscorbot 1 50 0 ./initial_config.json
./test_edscorbot 2 50 0 ./initial_config.json
./test_edscorbot 3 50 0 ./initial_config.json
./test_edscorbot 4 50 0 ./initial_config.json
./test_edscorbot 5 50 0 ./initial_config.json

sleep 0.001

./test_edscorbot 1 0 0 ./initial_config.json
./test_edscorbot 2 0 0 ./initial_config.json
./test_edscorbot 3 0 0 ./initial_config.json
./test_edscorbot 4 0 0 ./initial_config.json
./test_edscorbot 5 0 0 ./initial_config.json

sleep 0.001

./test_edscorbot 1 -50 0 ./initial_config.json
./test_edscorbot 2 -50 0 ./initial_config.json
./test_edscorbot 3 -50 0 ./initial_config.json
./test_edscorbot 4 -50 0 ./initial_config.json
./test_edscorbot 5 -50 0 ./initial_config.json

sleep 0.001

./test_edscorbot 1 -100 0 ./initial_config.json
./test_edscorbot 2 -100 0 ./initial_config.json
./test_edscorbot 3 -100 0 ./initial_config.json
./test_edscorbot 4 -100 0 ./initial_config.json
./test_edscorbot 5 -100 0 ./initial_config.json