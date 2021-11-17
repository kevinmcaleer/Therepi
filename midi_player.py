# TherePi
# Kevin McAleer
# 12 November 2021
# LICENSE: https://unlicense.org
# Mido Midi Sender

import mido
from mido import Message
from mido.sockets import connect
from time import sleep
from mido.midifiles import MidiFile

HOST = '192.168.1.229'
PORT = 8080
FILENAME = 'tocata.mid'


output = connect(HOST, PORT)

print("Starting Midi Player")
for msg in MidiFile('tocata.mid').play():
    print(msg)
    output.send(msg)


# while True:
#     for note in notes:
#         msg = Message('note_on', note=note)
#         output.send(msg)
#         print(msg)
#         sleep(.5)