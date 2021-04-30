

from stmpy import Machine, Driver
from os import system
import os
import time

import pyaudio
import wave
import io
        
class Player:
    def __init__(self, driver):

        self.stm_driver = driver

        t0 = {'source': 'initial', 'target': 'ready'}
        t1 = {'trigger': 'start', 'source': 'ready', 'target': 'playing'}
        t2 = {'trigger': 'done', 'source': 'playing', 'target': 'ready'}

        s_playing = {'name': 'playing', 'do': 'play(*)'}

        self.stm = Machine(name='player', transitions=[t0, t1, t2], states=[s_playing], obj=self)
        self.stm_driver.add_machine(self.stm)


    def play(self, audio):
        #filename = 'output.wav'
        file = io.BytesIO(audio)

        # Set chunk size of 1024 samples per data frame
        chunk = 1024  

        # Open the sound file 
        wf = wave.open(file, 'rb')

        # Create an interface to PortAudio
        p = pyaudio.PyAudio()

        # Open a .Stream object to write the WAV file to
        # 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # Read data in chunks
        #data = wf.readframes(chunk)
        data = wf.readframes(wf.getnframes())

        # Play the sound by writing the audio data to the stream
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)

        # Close and terminate the stream
        stream.close()
        p.terminate()