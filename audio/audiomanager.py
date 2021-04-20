from stmpy import Machine, Driver
import logging
from threading import Thread
import json

class AudioManager:
    """
    State Machine for an audio manager.
    This is the support object for a state machine that models a single timer.
    """
    def __init__(self, name, duration, component):
        self._logger = logging.getLogger(__name__)
        self.name = name
        self.duration = duration
        self.component = component

        t0 = {'source': 'initial', 'target': 'ready'}
        t1 = {'trigger': 'start', 'source': 'ready', 'target': 'recording'}
        t2 = {'trigger': 'done', 'source': 'recording', 'target': 'processing'}
        t3 = {'trigger': 'done', 'source': 'processing', 'target': 'ready'}

        s_recording = {'name': 'recording', 'do': 'record()', "stop": "stop()"}
        s_processing = {'name': 'processing', 'do': 'process()'}

        self.stm = Machine(name=self.name, transitions=[t0, t1, t2], states=[s_recording, s_processing], obj=self)
        self.component.stm_driver.add_machine(self.stm)
