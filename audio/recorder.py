from stmpy import Machine, Driver
from os import system
import os
import time
import logging

import pyaudio
import wave
import io
        
class Recorder:
    def __init__(self, driver):

        self.stm_driver = driver

        self.recording = False
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1
        self.fs = 44100  # Record at 44100 samples per second
        self.filename = "output.wav"
        
        self._logger = logging.getLogger(__name__)

        t0 = {'source': 'initial', 'target': 'ready'}
        t1 = {'trigger': 'start', 'source': 'ready', 'target': 'recording'}
        t2 = {'trigger': 'done', 'source': 'recording', 'target': 'processing'}
        t3 = {'trigger': 'done', 'source': 'processing', 'target': 'ready'}

        s_recording = {'name': 'recording', 'do': 'record()', "stop": "stop()", 'start': 'defer'}
        s_processing = {'name': 'processing', 'do': 'process()', 'start': 'defer'}

        self.stm = Machine(name="recorder", transitions=[t0, t1, t2, t3], states=[s_recording, s_processing], obj=self)
        self.stm_driver.add_machine(self.stm)

    def record(self):
        print("recording...")
        self.p = pyaudio.PyAudio() 

        stream = self.p.open(format=self.sample_format,
                channels=self.channels,
                rate=self.fs,
                frames_per_buffer=self.chunk,
                input=True)
        self.frames = []  # Initialize array to store frames
        # Store data in chunks
        self.recording = True
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)
        print("done recording")
        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()
        
    def stop(self):
        print("stop")
        self.recording = False
    
    def process(self):
        print("processing")
        # Save the recorded data as a WAV file

        writer_file = io.BytesIO() # This emulates an actual file

        wf = wave.open(writer_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print("done processing")

        content = writer_file.getvalue() # TODO: remember to change this back!!
        #content = "Audio data here"
        self.stm_driver.send("recordingFinished", "HospiTalkie", args=[content])
        print("recording sent")
    