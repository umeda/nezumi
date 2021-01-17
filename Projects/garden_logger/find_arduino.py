from serial.tools import list_ports  # pip uninstall serial; pip install pyserial
from serial import Serial
from serial import STOPBITS_ONE

for port in list(list_ports.comports()):
    print(port.hwid)
    if port.hwid.startswith('USB VID:PID=0403:6001'):
        print('Arduino on: ' + port.device)
        arduinoPort = port.device

serialPort = Serial(port=arduinoPort, baudrate=9600, bytesize=8, timeout=2, stopbits=STOPBITS_ONE)


serialString = ""  # Used to hold data coming over UART


while(1):

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # Print the contents of the serial data
        print(serialString.decode('Ascii'))

        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        # serialPort.write(b"Thank you for sending data\n")
    # see if there are any commands in the keyboard buffer.



