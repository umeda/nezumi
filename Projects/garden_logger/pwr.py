 #!/usr/bin/python
import gpizero as GPIO , time
from datetime import datetime

redLED=35
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLED, GPIO.IN)

powerlow=0
while True:
        if(GPIO.input(redLED)==0):
                print('Power less than 4.63v at ' + str(datetime(now())))
                powerlow += 1
        else:
                powerlow =0
                print('Power OK at ' + str(datetime(now())))
        if (powerlow  > 3):
                 print("Low power for " + str(powerlow) + " seconds")
        time.sleep(1)
