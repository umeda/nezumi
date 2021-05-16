from flask import Flask  # https://flask.palletsprojects.com/en/1.1.x/
from flask import render_template

from serial.tools import list_ports  # pip uninstall serial; pip install pyserial
from serial import Serial  # https://pyserial.readthedocs.io/en/latest/shortintro.html
from serial import STOPBITS_ONE
from time import sleep
import threading
from pprint import pprint

import RPi.GPIO as GPIO
import time
import os


# would it be better to use gevent? Maybe not.
app = Flask(__name__)

for port in list(list_ports.comports()):
    print(port.hwid)
    if port.hwid.startswith('USB VID:PID=0403:6001'):  # change this if using something other than Seeeduino.
        print('Arduino on: ' + port.device)
        arduinoPort = port.device


serialString = ""  # Used to hold data coming over UART
loggerData = ""
params = []
values = []

 

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

 

def Shutdown(channel):
    # blink shutdown led
    os.system("sudo shutdown -h now")

GPIO.add_event_detect(21, GPIO.FALLING, callback=Shutdown, bouncetime=2000)


def monLogger():
    global loggerData
    global params
    global values
    serialPort = Serial(port=arduinoPort, baudrate=9600, bytesize=8, timeout=2, stopbits=STOPBITS_ONE)
    # print('flushing input')
    # serialPort.flushInput()
    while(1):
        sleep(10)
        print('check for blah')
        # print(threading.currentThread().getName())
        # print(loggerData)
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):
            # print('threads: ' + str(threading.active_count()))
            # for thread in threading.enumerate():
            #     print(thread.name)
            # Read data out of the buffer until a carriage return / new line is found
            serialString = ''
            loggerData = ''
            serialString = serialPort.readline()
            # Print the contents of the serial data
            print(serialString.decode('Ascii'))
            loggerData = serialString.decode('Ascii')
            data = serialString.decode('Ascii').split(',')
            # better do some error checking here.
            if data[0] == 'msg':
                loggerData = data[1]
            else:
                numMeasurements = int((len(data) - 1)/2)
                print(numMeasurements)
                params = data[1:numMeasurements + 1]
                values = data[numMeasurements + 1:(numMeasurements * 2) + 1]
                pprint(params)
                pprint(values)
                # check for low voltage - if low for more than an hour,
                # call the shutdown routine.
            # loggerData = serialString.decode('Ascii')
            print('blah')
            # Tell the device connected over the serial port that we recevied the data!
            # The b at the beginning is used to indicate bytes!
            # serialPort.write(b"Thank you for sending data\n")
            # see if there are any commands in the keyboard buffer.


print('ZUUL')
# for thread in threading.enumerate():
#     print(thread.name)
# dataAcq = threading.Thread(target=monLogger)
# dataAcq.start()
# dataAcq.join()
# gotta have this or the serial read gets corrupted.
# but if this is here, web server never starts


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cakes')
def cakes():
    return render_template('cakes.html')


@app.route('/hello/<name>')
def hello(name):
    global loggerData
    return render_template('page.html', name=name, headers=params, datas=values)


# if __name__ == '__main__':

#     print("starting server")
#     app.run(debug=True, host='0.0.0.0')
print('starting data acq')
dataAcq = threading.Thread(target=monLogger)
dataAcq.start()
print("starting server")
app.run(debug=False, host='0.0.0.0')  # debug=False should prevent restart and doubling dataAcq
