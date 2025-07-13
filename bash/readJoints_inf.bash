#!/bin/bash

if [ -z "$1" ]
  then
    echo "Introduzca la cantidad de espera entre sondeos"
    exit
fi


for((i=0; ;++i)); do
    ./readJoints.bash >> log.txt
    sleep $1
done

