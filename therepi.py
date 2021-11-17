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

HOST = '192.168.1.229'
PORT = 8080

min_distance = 5 # cm
max_distance = 50 # cm

# The two rangefinders
volume = DistanceSensor(echo=24, trigger=25)
pitch = DistanceSensor(echo=22, trigger=23)

def map(x, in_min, in_max, out_min, out_max):
    """ Maps the value x from the input range to the output range """
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def distance_to_frequency(distance, min, max):
    """ Maps the distance to the frequency """
    
    if distance in range(min,max+1):
        frequency = map(distance, min, max, 60, 120)
        return frequency
    else:
        return None

def distance_to_velocity(distance, min, max):
    """ converts distance to note velocity """
    if distance in range(min,max+1):
        velocity = map(distance, min, max, 0, 127)
        return velocity
    else:
        return None

def distance_to_note(distance):
    """ Converts the distance read from the range finder to a note """
    note = frequency_to_midi(distance)
    print("distance", distance, "note", note)
    return note

output = connect(HOST, PORT)

print("Starting TherePi Sender")
last_note = 0
last_volume = 0
note = 0
last_frequency = 0
while True:
    try:
        distance = pitch.distance
        vol = volume.distance
        
        distance = int(distance *100)
        vol = int(vol * 100)
        
#         print("distance", distance, "volume", vol)
        #velocity = 127
#         print("d", distance, "v",vol)
        frequency = distance_to_frequency(distance, min_distance, max_distance)
        velocity = distance_to_velocity(vol, min_distance, max_distance)
#         print("freq",frequency, "velocity",velocity)
        #print('frequency',frequency, 'last_frequency', last_frequency)
        if (frequency is None) and (frequency != last_frequency):
            msg = Message('note_off', note=note)
            output.send(msg)
            print(msg)
            last_frequency = frequency
        
        if (frequency is not None) and (velocity is not None):
#             print("freq",frequency, "velocity",velocity)
            
            note = frequency_to_midi(frequency)
            if note != last_note:
                msg = Message('note_off', note=last_note)
                output.send(msg)
                print(msg)
                sleep(0.001)
                msg = Message('note_on', note=note, velocity=velocity, time=0)
                output.send(msg)
                print(msg)
#             else:
#                 msg = Message('note_on',note=note)
#             if velocity != last_volume:
#                 msg.copy(velocity=velocity)
#                 output.send(msg)
#                 print(msg)
            last_note = note
            last_volume = velocity
            sleep(0.25)
            
        # for note in notes:
        #     msg = Message('note_on', note=note, velocity=127, time=0)
        #     output.send(msg)
        #     print(msg)
        #     sleep(0.5)
        #     # output.send(Message('note_off', note=note))
    except KeyboardInterrupt:
        output.close()
        break
