#!/bin/bash

#Read position from a joint
#Usage: ReadJoint.bash <joint>


declare -A addressPerJoint
addressPerJoint[1]=0xF1
addressPerJoint[2]=0xF2
addressPerJoint[3]=0xF3
addressPerJoint[4]=0xF4
addressPerJoint[5]=0xF5
addressPerJoint[6]=0xF6

j=$1

address=${addressPerJoint[$j]}

data=`printf "0x00%02x0000" ${address}`


ret=`devmem $data`

echo $ret