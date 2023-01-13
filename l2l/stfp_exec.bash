#!/bin/bash


#Download trajectory file
#$1 --> Name of trajectory file in target machine 
#$2 --> Name of counters file to write
#$3 --> Name of xyz file to write
#$4 --> Folder in sftp/local server 
traj=$1

if [ -z "$2" ]
  then
    counters="tmp_count.npy"
    else
    counters=$2

fi

if [ -z "$3" ]
  then
    xyz="out_xyz.npy"
    else
    xyz=$3

fi
if [ -z "$4" ]
  then
    echo "Please specify a directory in which to store data, both remotely and locally"
   exit 1
    else
    dir=$4
fi



mkdir $dir
sftp -i /home/enrique/sftp/id_rsa USEtrans@figipc180.tugraz.at:TRANSFER/ <<< $'get '"$dir/$traj $dir/$traj" 

python3.8 execute_trajectory.py -c -cont "$dir/$counters"  "$dir/$traj"
python3.8 cont_to_xyz.py -o "$xyz"  "$dir/$counters"


sftp -i /home/scorbot_admin/Py-EDScorbotTool/l2l/sftp/id_rsa USEtrans@figipc180.tugraz.at:TRANSFER/ <<< $'mkdir '"$dir" 
sftp -i /home/scorbot_admin/Py-EDScorbotTool/l2l/sftp/id_rsa USEtrans@figipc180.tugraz.at:TRANSFER/ <<< $'put '"$dir/$counters $dir/$counters"
sftp -i /home/scorbot_admin/Py-EDScorbotTool/l2l/sftp/id_rsa USEtrans@figipc180.tugraz.at:TRANSFER/ <<< $'put '"$dir/$xyz $dir/$xyz"