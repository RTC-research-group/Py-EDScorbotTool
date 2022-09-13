import sys
import paho.mqtt.client as mqtt
from argparse import ArgumentParser
from tqdm import  tqdm


#Send trajectory and wait for responses, until a 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global traj_name
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("EDScorbot/trajectory")
    topic = "/EDScorbot/commands"
    msg = "[1,S,{}]".format(traj_name)
    
    client.publish(topic,msg,qos=0)
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    parsed = msg.payload.decode('utf8').lstrip('[').rstrip(']').split(',')
    
    t.update()
    global i
    i+=1
    
    if i >499:
        sys.exit()
   
    #print(msg.topic+" "+str(msg.payload))


parser = ArgumentParser(description="Remote trajectory control/monitorization")
parser.add_argument("-t","--trajectory",type=str,help="Name of the trajectory file to execute")

args = parser.parse_args()
global traj_name
global i
i = 0
traj_name = args.trajectory

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.104", 1883, 60)
t = tqdm(total=500)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


