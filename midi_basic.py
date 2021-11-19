# midi_basic - A Basic Midi test program
# Kevin McAleer 14 November 2021

# Import some libraries
import mido
from mido import Message
from time import sleep

# Connect to local midi environment
IAC = 'IAC Driver Bus 1'
port = mido.open_output(IAC)

# Create some music notes
notes = [60,65,70,61,62]

while True:
    for note in notes:
        msg = Message('note_on', note=note)
        port.send(msg)
        print(msg)
        sleep(.5)

