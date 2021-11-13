import mido
from mido import Message
from mido.ports import EchoPort
from time import sleep

IAC = 'IAC Driver Bus 1'
port = mido.open_output(IAC)
msg = Message('note_on', note=60)

notes = [60,65,70,61,62]

while True:
    for note in notes:
        port.send(Message('note_on', note=note))
        print(msg)
        sleep(.5)