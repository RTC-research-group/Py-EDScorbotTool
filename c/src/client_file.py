import socket
import time
from argparse import ArgumentParser

if __name__ == "__main__":


    parser = ArgumentParser(description="File sender")
    parser.add_argument("file",type=str,help="File to be sent")
    parser.add_argument("--host","-H",type=str,help="IP or domain name to send the file to",default="150.214.140.189")
    parser.add_argument("--port","-p",type=int,help="Port to connect to in the destination machine",default=9999)
    parser.add_argument("--filename","-f",type=str,help="Name of the file to be written in the destination machine",default="dest.npy")
    args = parser.parse_args()
    
    HOST = args.host
    PORT = args.port

    f = open(args.file,"rb")
    data = f.read()
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        #comm = "[4]"
        sock.sendall(bytes(args.filename,encoding="utf-8"))
        time.sleep(1)
    
        received = sock.recv(1024)
        received = received.decode("utf-8")
        if received=="[OK]":
            print("Name sent correctly")
            print ("Sent:     {}".format(args.filename))
            print ("Received: {}".format(received))
        
        sock.sendall(bytes(data))
        time.sleep(1)
        received = sock.recv(1024)
        received = received.decode("utf-8")
        if received=="[OK]":
            print("Data sent correctly")
            print ("Sent:     {}".format(data))
            print ("Received: {}".format(received))

        
        else:
            print("Something went wrong during data transmission")
            print ("Received: {}".format(received))

        

    finally:
        sock.close()


