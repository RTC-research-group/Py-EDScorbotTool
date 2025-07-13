from nis import match
import sys
import os
# setting path
sys.path.append('../python')

#from pyEDScorbotTool import pyEDScorbotTool
import argparse
import pyEDScorbotTool.utils.transformations.omegas_to_angles as omegas_to_angles
import pyEDScorbotTool.utils.transformations.angles_to_json as angles_to_json
import numpy as np
#from DirecKinScorbot import DirecKinScorbot
import paho.mqtt.client as mqtt
import tqdm
import json as j

TOPIC = "/EDScorbot/commands"
global RUNNING
RUNNING = 1



def on_connect(client, userdata, flags, rc):
        global traj_name
        global n
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("EDScorbot/trajectory")       
 
        
        

        # The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
        
        parsed = msg.payload.decode('utf8').lstrip('[').rstrip(']').split(',')
        #print(parsed)
        #t.update()
        #global i
        #i+=1

        j1 = int(parsed[0])
        j2 = int(parsed[1])
        j3 = int(parsed[2])
        j4 = int(parsed[3])
        j5 = int(parsed[4])
        j6 = int(parsed[5])
        ts = int(parsed[6])
        iter = int(parsed[7])
        
        
        userdata['pos_data'].append([j1,j2,j3,j4,j5,j6,ts])

        if int(iter) < 0:
            arr = np.array(userdata['pos_data'])
            savename = userdata['savename']
            #savename = input("Name for output file")
            np.save(savename,arr[:-1])
            userdata['progressbar'].close()
            print("Output file has been saved to {}".format(savename))
            global RUNNING
            RUNNING = 0
            #np.save("output_data.npy",arr[:-1])
            
            #sys.exit()
            
        if iter > 0:
            userdata['progressbar'].update()
            
        #print(msg.topic+" "+str(msg.payload))

def open_mqtt(ip):

        
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        
        client.connect(ip, 1883, 60)
        client.loop_start()
        
        return client
    
    
def close_mqtt(mqtt_client):
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        
        pass

def send_trajectory(args):
    #
    #filename = filedialog.askopenfile(mode="r")
    filename = args.trajectory
    id = args.identity
    real_name = filename.rstrip().lstrip().split('/')[-1]
    ref_filename = real_name.split('.')[0] + "_6dims.json"
    #cmd = "python3 mqtt/client_traj.py -t {} -n 500 &".format(real_name)
    #################################
    #MUST BE PARAMETERIZED CORRECTLY#
    #################################
    traj = np.load(args.trajectory,allow_pickle=True)
    if args.conv:#Esto significa que hay que hacer la conversión
        traj = omegas_to_angles.w_to_angles(traj)
        pass
    orig_traj = traj
    traj = angles_to_json.angles_to_json(orig_traj)
    #traj2 = angles_to_json.angles_to_json(orig_traj,visual = False)
    n = traj.shape[0]
    f = open(ref_filename,"w")
    js = j.dump(traj.tolist(),f,indent=4)
    f.close()

    cmd = "scp -i {} {} root@192.168.1.115:/home/root/{}".format(id,ref_filename,ref_filename)
    os.system(cmd)
    mqtt_client = open_mqtt("192.168.1.104")
    pb = tqdm.tqdm(file=sys.stdout)
    d = {
        'pos_data':[],
        'progressbar':pb,
        'savename':args.counters
    }
    d['progressbar'].total = n
    mqtt_client.user_data_set(d)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    msg = "[1,S,/home/root/{},{}]".format(ref_filename,n)
    
    mqtt_client.publish(TOPIC,msg,qos=0)
    #os.system(cmd)
    return mqtt_client


if __name__== '__main__':
    #global RUNNING
    parser = argparse.ArgumentParser(description="Trajectory execution tool to include ED-Scorbot in the L2L loop",allow_abbrev=True)
    parser.add_argument("trajectory",type=str,help="Trajectory file in NumPy format. By default, trajectories should be specified in angular velocities")
    parser.add_argument("--conv","-c",help="Specify this flag to indicate that the input trajectory should be converted to angles",action="store_true",default=False)
    parser.add_argument("--counters","-cont",type=str,help="Name of the file in which we will store the time-stepped output in counter format",default=None)
    parser.add_argument("identity",type=str,help="Name of key file to upload the trajectory file")

    #parser.add_argument("--position","-xyz",type=str,help="Name of the file in which we will store the time-stepped output in xyz format",default=None)

    args = parser.parse_args()

    

    
    
    mqtt_client = send_trajectory(args)
    #1.- Inicializacion cliente mqtt
    #2.- Inicializacion variables globales --> tqdm, userdata (para mqtt)
    
    while(RUNNING):
        pass
    
    close_mqtt(mqtt_client)
    
    #Asumimos que el robot ha hecho el home previamente y que todo esta inicializado
    
    
    
    