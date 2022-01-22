#!/usr/bin/python
# import time
import Adafruit_DHT
# import pycurl
# from StringIO import StringIO
from sys import exc_info
import requests

from pathlib import Path

Path('/home/pi/pyblah123.txt').touch()

sensor_22 = Adafruit_DHT.DHT22
sensor_11 = Adafruit_DHT.DHT11

hires_pin = 4
lores_pin = 17

hires__temperature = None
hires_humidity = None
lores_temperature = None
lores_humidity = None

try:
    hires_humidity, hires_temperature = Adafruit_DHT.read_retry(sensor_22, hires_pin)
except:  # Catch all exceptions
    e = exc_info()[0]
    print("Error: %s" % e)
try:
    lores_humidity, lores_temperature = Adafruit_DHT.read_retry(sensor_11, lores_pin)
except:  # Catch all exceptions
    e = exc_info()[0]
    print("Error: %s" % e)

url = 'https://maker.ifttt.com/trigger/temp_001/with/key/XXXXXXXX-XXXXXXXXXXXX'
msg = ""

if hires_humidity is not None and hires_temperature is not None:
    hires_temperature = hires_temperature * 9 / 5 + 32
    print('HiRes: Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format(hires_temperature, hires_humidity))
    hrt = "{0:.1f}".format(hires_temperature)
    hrh = "{0:.1f}".format(hires_humidity)
    msg += '\nHiRes ' + hrt + ' ' + u'\N{DEGREE SIGN}'.encode('utf-8') + 'F, ' + hrh + ' %RH'
else:
    print('\nFailed to get HiRes reading')
    msg += '\nHiRes Error'

if lores_humidity is not None and lores_temperature is not None:
    lores_temperature = lores_temperature * 9 / 5 + 32
    print('LoRes: Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format(lores_temperature, lores_humidity))
    lrt = "{0:.1f}".format(lores_temperature)
    lrh = "{0:.1f}".format(lores_humidity)
    msg += '\nLoRes ' + lrt + ' ' + u'\N{DEGREE SIGN}'.encode('utf-8') + 'F, ' + lrh + ' %RH'
else:
    print('Failed to get LoRes reading')
    msg += '\nLoRes Error/n'

json_msg = {"value1": msg}

print(msg)

resp = requests.post(url=url, data=json_msg)
print(resp.content)

# url += '&humidity=' + "{:.1f}".format(humidity)
# print(url)
# buffer = StringIO()
# c = pycurl.Curl()
# c.setopt(c.URL, url)
# c.setopt(c.WRITEDATA, buffer)
# c.perform()
# c.close()
# body = buffer.getvalue()
# print(body)

