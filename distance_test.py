from gpiozero import DistanceSensor
from time import sleep
pitch = DistanceSensor(trigger=27, echo=22)
while True:
    distance = pitch.distance
    print(distance*100)
    sleep(0.1)