import socket
import sys
import json

HOST, PORT = "localhost", 9999

#m ='{"id": 2, "name": "abc"}'
m = {"id": 2, "name": "abc"} # a real dict.


data = json.load(open(r"D:\Universidad\Master\Ondrive Cloud\OneDrive - UNIVERSIDAD DE SEVILLA\Trabajo\SMALL\Py-EDScorbotTool\initial_config.json"))
data = json.dumps(data)
# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data,encoding="utf-8"))


    # Receive data from the server and shut down
    received = sock.recv(1024)
    received = received.decode("utf-8")

finally:
    sock.close()

print ("Sent:     {}".format(data))
print ("Received: {}".format(received))
