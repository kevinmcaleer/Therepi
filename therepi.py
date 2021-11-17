# TherePi
# Kevin McAleer
# 12 November 2021
# LICENSE: https://unlicense.org
# Mido Midi TherePi

from gpiozero.input_devices import DistanceSensor
import mido
from mido import Message
from mido.sockets import connect
from time import sleep, time_ns
from pygame.midi import frequency_to_midi
from gpiozero import DistanceSensor

HOST = '192.168.1.219'
PORT = 8080

# The two rangefinders
volume = DistanceSensor(echo=20, trigger=21)
pitch = DistanceSensor(echo=22, trigger=27)

def map(x, in_min, in_max, out_min, out_max):
    """ Maps the value x from the input range to the output range """
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def distance_to_frequency(distance):
    """ Maps the distance to the frequency """
    frequency = map(distance, 5, 50, 60, 120)
    return frequency

def distance_to_velocity(distance):
    velocity = map(distance, 5, 50, 0, 127)
    return velocity

def distance_to_note(distance:float):
    """ Converts the distance read from the range finder to a note """
    note = frequency_to_midi(distance)
    return note

output = connect(HOST, PORT)

print("Starting TherePi Sender")
while True:
    try:
        distance = pitch.distance
        sleep(0.1)
        # velocity = volume.distance
        velocity = 127
        frequency = distance_to_frequency(distance)
        note = frequency_to_midi(frequency)
        msg = Message('note_on', note=note, velocity=velocity, time=0)
        output.send(msg)
    except KeyboardInterrupt:
        output.close()
        break
