#!/bin/bash


#Download trajectory file
#$1 --> Name of trajectory file in target machine 
#$2 --> Name of key file for scp authentication
#$3 --> Name of counters file to write
#$4 --> Name of xyz file to write
#$5 --> Folder in sftp/local server

if [ -z "$1" ]
  then
    echo "Please specify a trajectory file in the correct format"
   exit 1
    else
    traj=$1
fi

if [ -z "$2" ]
  then
    echo "Please specify a key file to use for scp authentication"
   exit 1
    else
    i=$2
fi

if [ -z "$3" ]
  then
    counters="tmp_count.npy"
    else
    counters=$3

fi

if [ -z "$4" ]
  then
    xyz="out_xyz.npy"
    else
    xyz=$4

fi
if [ -z "$5" ]
  then
    echo "Please specify a directory in which to store data, both remotely and locally"
   exit 1
    else
    dir=$5
fi



mkdir -p $dir
sftp -i /home/enrique/sftp/id_rsa USEtrans@figipc180.tugraz.at:TRANSFER/ <<< $'get '"$dir/$traj $dir/$traj" 

python3 execute_trajectory.py -c -cont "$dir/$counters"  "$dir/$traj" "$i"
cont_to_xyz -np -o "$dir/$xyz"  "$dir/$counters"


sftp -i /home/enrique/sftp/id_rsa USEtrans@figipc180.tugraz.at:TRANSFER/ <<< $'mkdir '"$dir" 
sftp -i /home/enrique/sftp/id_rsa USEtrans@figipc180.tugraz.at:TRANSFER/ <<< $'put '"$dir/$counters $dir/$counters"
sftp -i /home/enrique/sftp/id_rsa USEtrans@figipc180.tugraz.at:TRANSFER/ <<< $'put '"$dir/$xyz $dir/$xyz"