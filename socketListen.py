import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(('127.0.0.1', 5005))

while 1:
    data = client_socket.recvfrom(1024)
    if(data == 'q' or data =='Q'):
        client_socket.close()
        print("Error!\n")
        break;
    else:
        print("RECIEVED:", data)
