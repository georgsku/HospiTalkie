from stmpy import Machine, Driver
import logging
from threading import Thread
import json
import pyaudio
import wave


class AudioManager:
    """
    State Machine for an audio manager. Handle file actions for audio.
    """
    def __init__(self):

        self.stm_driver = driver

        t0 = {'source': 'initial', 'target': 'ready'}
        t1 = {'trigger': 'saveFile', 'source': 'ready', 'target': 'writing'}
        t2 = {'trigger': 'done', 'source': 'processing', 'target': 'ready'}
        t3 = {'trigger': 'deleteFile', 'source': 'writing', 'target': 'deleting'}
        t2 = {'trigger': 'done', 'source': 'deleting', 'target': 'ready'}

        s_writing = {'name': 'writing', 'do': 'save(*)'}
        s_deleting = {'name': 'deleting', 'do': 'delete(*)'}

        self.stm = Machine(name="AudioManager", transitions=[t0, t1, t2, t3], states=[s_writing, s_deleting], obj=self)
        self.stm_driver.add_machine(self.stm)

    def save(self, fileName, data):
        #TODO: save to new unique file after each time... Do we need some form of DB? Maybe just a large dict with filenames and metadata...??
        filename = fileName + ".wav"
        
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 1
        self.fs = 44100  # Record at 44100 samples per second
        self.p = pyaudio.PyAudio() 

        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(data)
        wf.close()

    def delete(self, fileName):
        #todo: delete unused files.
        print("Deleting file...")