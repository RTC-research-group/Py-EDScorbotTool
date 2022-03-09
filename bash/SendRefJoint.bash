#!/bin/bash

#Send a reference to a joint
#usage: SendRefJoint.bash <joint> <reference>

declare -A addressPerJoint
addressPerJoint[1]=0x02
addressPerJoint[2]=0x22
addressPerJoint[3]=0x42
addressPerJoint[4]=0x62
addressPerJoint[5]=0x82
addressPerJoint[6]=0xA2



j=$1
ref=$2

address=${addressPerJoint[$j]}
ref_high="$(((${ref} >> 8) & 0xff ))"
ref_low="$(((${ref}) & 0xff ))"

data=`printf "0x00%02x%02x%02x" ${address} ${ref_high} ${ref_low}`

#echo $data
devmem $data