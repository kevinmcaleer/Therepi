# YouTube
Here is the build Video!

[![https://img.youtube.com/vi/MWPnnRE1kR8/01.jpg](https://img.youtube.com/vi/MWPnnRE1kR8/0.jpg)](https://youtu.be/MWPnnRE1kR8)

# TherePi
The Raspberry Pi based Theremin like Musical Instrument, built with two HC-SR04 Range Finders. Its pronouced Thera (as in Therapy), Pie - Thera-Pie.

Software Architecture
TherePi uses the Python Mido library, to send midi data from the Raspberry Pi Zero across to another computer running Garageband, to produce sounds based on the distances read from the two range finders; one for volume, and one for pitch.

Unlike the Theremin, the TherePi can auto-tune to specific notes, making it slightly easier to play.


# The files
- `midi_basic.py` is a simple program to test that midi is working on your computer
- `midi_player.py` is a simply midi file player - it will read in the contents of the file and send it to the `midi_receiver.py` server on the local machine
- `midi_receiver.py` listens for connections and then plays the midi messages received on the local machine
- `midi_sender.py` sends a couple of test notes to the midi server specified in the `HOST` variable
- `therepi.py` is the main program for running with the therepi hardware - it will use the two range finders to specic which notes to play and how loud to play then depending on the distance read from each sensor
