import socket
import sys
import time

HOST, PORT = "localhost", 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
for x in range(0, 10):
    print("Send command")
    s.send(b'refJ1 50')
    print("Receive confirmation")
    print(str(s.recv(1000)))
    print(x)
    time.sleep(2)
