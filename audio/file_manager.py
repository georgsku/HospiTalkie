from stmpy import Machine, Driver
import logging
from threading import Thread
import json
import pyaudio
import wave
import os


class FileManager:
    """
    State Machine for an audio manager. Handle file actions for audio.
    """
    def __init__(self, driver):

        self.stm_driver = driver

        t0 = {'source': 'initial', 'target': 'ready'}
        t1 = {'trigger': 'saveFile', 'source': 'ready', 'target': 'writing'}
        t2 = {'trigger': 'done', 'source': 'writing', 'target': 'ready'}
        t3 = {'trigger': 'deleteFile', 'source': 'ready', 'target': 'deleting'}
        t4 = {'trigger': 'done', 'source': 'deleting', 'target': 'ready'}

        s_writing = {'name': 'writing', 'do': 'save(*)', 'saveFile': 'defer', 'deleteFile': 'defer',  }
        s_deleting = {'name': 'deleting', 'do': 'delete(*)', 'saveFile': 'defer', 'deleteFile': 'defer'}

        self.stm = Machine(name="fileManager", transitions=[t0, t1, t2, t3, t4], states=[s_writing, s_deleting], obj=self)
        self.stm_driver.add_machine(self.stm)

    def save(self, fileName, data):
        #TODO: save to new unique file after each time... Do we need some form of DB? Maybe just a large dict with filenames and metadata...??
        filename = fileName + ".wav"
        f = open('./Messages/' + filename, 'wb')
        f.write(data)
        f.close()

    def delete(self, path):
        #todo: delete unused files.
        print("Deleting file...")
        if os.path.exists(path):
            os.remove(path)
        else:
            print("The file does not exist")