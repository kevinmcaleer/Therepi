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
# from pygame.midi import frequency_to_midi
from gpiozero import DistanceSensor

HOST = '192.168.1.229'
PORT = 8080

min_distance = 15 # cm
max_distance = 50 # cm

# The two rangefinders
volume = DistanceSensor(echo=24, trigger=25)
pitch = DistanceSensor(echo=22, trigger=23)

def map(x, in_min, in_max, out_min, out_max):
    """ Maps the value x from the input range to the output range """
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


# def distance_to_note(distance, min, max):
#     """ Maps the distance to the note """
    
#     if distance in range(min,max+1):
#         d_note = int(map(distance, min, max, 60, 72))
#         return d_note
#     else:
#         return None

def map_distance(distance, inmin, inmax, outmin, outmax):
    """ converts distance to note pitch or velocity """

    if distance in range(min,max+1):
        velocity = map(distance, min, max, outmin, outmax)
        return velocity
    else:
        return None

# def distance_to_frequency(distance):
#     """ Maps the distance to the frequency """
#     frequency = map(distance, 5, 50, 60, 120)
#     return frequency

# def distance_to_velocity(distance):
#     velocity = map(distance, 5, 50, 0, 127)
#     return velocity
#     return note

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

        frequency = map_distance(distance, min_distance, max_distance, 60, 72)
        velocity = map_distance(vol, min_distance, max_distance, 0, 127)

        if frequency is None:
            msg = Message('note_off', note=last_note)
            output.send(msg)
            print(msg)
            last_frequency = frequency
            note = 0
        
        if (frequency is None) and (frequency != last_frequency):
            msg = Message('note_off', note=note)
            output.send(msg)
            print(msg)
            last_frequency = frequency
        
        if (frequency is not None):
#             print("freq",frequency, "velocity",velocity)
            if velocity == None:
                velocity = 127
            #note = frequency_to_midi(frequency)
            note = frequency
            if note != last_note:
                msg = Message('note_off', note=last_note)
                output.send(msg)
                print(msg)
                sleep(0.0001)
                msg = Message('note_on', note=note, velocity=velocity, time=0)
                output.send(msg)
                print(msg)
#             else:
#                 msg = Message('note_on',note=note)
            if velocity != last_volume:
                msg.copy(velocity=velocity)
                output.send(msg)
                print(msg)
            last_note = note
            last_volume = velocity
        last_frequency = frequency
        sleep(0.001)
            
        # for note in notes:
        #     msg = Message('note_on', note=note, velocity=127, time=0)
        #     output.send(msg)
        #     print(msg)
        #     sleep(0.5)
        #     # output.send(Message('note_off', note=note))

    except KeyboardInterrupt:
        output.close()
        break
