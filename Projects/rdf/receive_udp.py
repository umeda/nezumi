import socket
from time import time
# maybe need numpy
from 
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
 
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
kount = 0 
timecurr = time()

while True:
    kount += 1
    data, addr = sock.recvfrom(4) # buffer size is 1024 bytes
    timeold = timecurr
    timecurr = time()
    timedelta = timecurr - timeold
    print(f"received message {kount}: {data}")
    