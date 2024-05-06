import dht
from machine import Pin
sensor = dht.DHT11(Pin(22))
#sensor = dht.DHT22(Pin(22))

sensor.measure() 
sensor.temperature()
sensor.humidity()