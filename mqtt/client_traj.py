import paho.mqtt.client as mqtt
import tqdm

#Send trajectory and wait for responses, until a 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("EDScorbot/trajectory")
    
    client.publish("/EDScorbot/commands","[1,U,urldeprueba]",qos=0)
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    parsed = msg.payload.decode('utf8').lstrip('[').rstrip(']').split(',')
    #print(parsed)
    t.update()
    #print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.104", 1883, 60)
t = tqdm.tqdm(total=500)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()