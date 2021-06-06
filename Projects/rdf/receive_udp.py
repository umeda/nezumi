import socket
from time import time
import numpy as np
from pprint import pprint
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
from engineering_notation import EngNumber

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
kount = 0 
timecurr = time()
deltas = np.full((20), 0.0)

while True:
    kount += 1
    data, addr = sock.recvfrom(4) # buffer size is 1024 bytes
    timeold = timecurr
    timecurr = time()
    deltas[0] = timecurr - timeold
    deltas = np.roll(deltas,-1)
    # pprint(deltas)
    # print(f"received message {kount}: {data}, {deltas[0]}")
    if kount > 20:
        print(f"avg = {EngNumber(np.mean(deltas))} , stdev = {EngNumber(np.std(deltas))}")
    