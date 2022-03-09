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

data1="0x00F10000"
data2="0x00F20000"
data3="0x00F30000"
data4="0x00F40000"
data5="0x00F50000"
data6="0x00F60000"

ret1=`devmem $data1`
ret2=`devmem $data2`
ret3=`devmem $data3`
ret4=`devmem $data4`
ret5=`devmem $data5`
ret6=`devmem $data6`


echo "$ret1,$ret2,$ret3,$ret4,$ret5,$ret6"