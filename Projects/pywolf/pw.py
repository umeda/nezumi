import sys
import socket
import select
import  aprslib
from pprint import pprint as pp
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 8001
BUFFER_SIZE = 1024
param = []

print('Listening for client...')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', TCP_PORT)
print('connecting to: ' + str(server_address))
sock.connect(server_address)
while(True):
    data = sock.recv(1024)
    print("Received: " + str(data))
    # print("Received: " + str(data.decode("utf-8")))
    # pp(aprslib.parse(data))
    # pp(aprslib.parse(data.decode("utf-8")))
