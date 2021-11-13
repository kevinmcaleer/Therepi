# TherePi
# Kevin McAleer
# 12 November 2021
# LICENSE: https://unlicense.org
# Mido Midi TherePi

import mido
from mido import Message
from mido.sockets import connect
from time import sleep, time_ns
from pygame.midi import frequency_to_midi
import gpiozero

HOST = 'localhost'
PORT = 8080

# The two rangefinders
volume_echo = gpiozero.Pin(2)
volume_trigger = gpiozero.Pin(3)

pitch_echo = gpiozero.Pin(20)
pitch_trigger = gpiozero.Pin(21)

def ping(trigger, echo):
    trigger.low()
    sleep(0.002)
    trigger.high()
    sleep(0.005)
    trigger.low()
    signalon = 0
    signaloff = 0
    while echo.value() == 0:
        signaloff = time_ns()
    while echo.value() == 1:
        signalon = time_ns()
    elapsed_time = signalon - signaloff
    # duration = elapsed_time
    distance = (elapsed_time * 0.343) / 2
    return distance 

def map(x, in_min, in_max, out_min, out_max):
    """ Maps the value x from the input range to the output range """
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def distance_to_frequency(distance):
    """ Maps the distance to the frequency """
    frequency = map(distance, 5, 40, 60, 120)
    return frequency

def distance_to_velocity(distance):
    velocity = map(distance, 5, 40, 0, 127)
    return velocity

def distance_to_note(distance:float):
    """ Converts the distance read from the range finder to a note """
    note = frequency_to_midi(distance)
    return note

output = connect(HOST, PORT)

print("Starting TherePi Sender")
while True:
    try:
        distance = ping(trigger=pitch_trigger, echo=pitch_echo)
        velocity = 127
        frequency = distance_to_frequency(distance)
        note = frequency_to_midi(frequency)
        msg = Message('note_on', note=note, velocity=velocity, time=0)
        output.send(msg)
        # for note in notes:
        #     msg = Message('note_on', note=note, velocity=127, time=0)
        #     output.send(msg)
        #     print(msg)
        #     sleep(0.5)
        #     # output.send(Message('note_off', note=note))
    except KeyboardInterrupt:
        output.close()
        break
