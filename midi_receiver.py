# TherePi
# Kevin McAleer
# 12 November 2021
# LICENSE: https://unlicense.org
# Mido Midi Receiver

import mido
from mido import Message
from mido.sockets import PortServer
# from midi.ports import port

HOST = 'localhost'
PORT = 8080

# Setup Midi Environment
IAC = 'IAC Driver Bus 1'
port = mido.open_output(IAC)

with PortServer(HOST, PORT) as server:
    print("TherePi Midi Receiver Server started...")
    while True:
        try:
            try:
                client = server.accept()
            except: 
                print("oops error caught")
            for message in client:
                try:
                    port.send(message)
                    print(message)
                except:
                    print("oops error caught")
        except KeyboardInterrupt:
            port.close()
            break