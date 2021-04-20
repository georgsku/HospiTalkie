import paho.mqtt.client as mqtt
import stmpy
import logging
from threading import Thread
import json
from appJar import gui
import mqttCommunication as mqtt_com

MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

MQTT_TOPIC_INPUT = 'ttm4115/team_3/command'
MQTT_TOPIC_OUTPUT = 'ttm4115/team_3/answer'


class TimerLogic:
    """
    State Machine for a named timer.

    This is the support object for a state machine that models a single timer.
    """

    def __init__(self, name, duration, component):
        self._logger = logging.getLogger(__name__)
        self.name = name
        self.duration = duration
        self.component = component

        def report_status():
            print("report status")
            self.component.mqtt_client.publish(MQTT_TOPIC_OUTPUT, "You have " + str(
                self.stm.get_timer('t') / 1000) + " seconds left on the " + str(self.name) + " timer.")
            print(self.stm.get_timer('t'))

        def timer_completed():
            print("t comp")
            self.component.mqtt_client.publish(MQTT_TOPIC_OUTPUT, "Your " + self.name + " timer is ready!")

        # TODO: build the transitions
        t0 = {'source': 'initial',
              'target': 'active'}

        # compound transition
        t1 = {'trigger': 'report',
              'source': 'active',
              'target': 'active',
              'function': report_status}

        # the other two regular transitions:
        t2 = {'trigger': 't',
              'source': 'active',
              'target': 'completed',
              'function': timer_completed}

        # the states:
        active = {'name': 'active',
                  'entry': 'start_timer("t", 5000)'}

        completed = {'name': 'completed'}

        self.stm = stmpy.Machine(name=self.name, transitions=[t0, t1, t2], obj=self, states=[active, completed])
        self.component.stm_driver.add_machine(self.stm)

        # TODO define functions as transition effetcs


class TimerManagerComponent:
    """
    The component to manage named timers in a voice assistant.

    This component connects to an MQTT broker and listens to commands.
    To interact with the component, do the following:

    * Connect to the same broker as the component. You find the broker address
    in the value of the variable `MQTT_BROKER`.
    * Subscribe to the topic in variable `MQTT_TOPIC_OUTPUT`. On this topic, the
    component sends its answers.
    * Send the messages listed below to the topic in variable `MQTT_TOPIC_INPUT`.

        {"command": "new_timer", "name": "spaghetti", "duration":50}

        {"command": "status_all_timers"}

        {"command": "status_single_timer", "name": "spaghetti"}

    """

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        """
        Processes incoming MQTT messages.

        We assume the payload of all received MQTT messages is an UTF-8 encoded
        string, which is formatted as a JSON object. The JSON object contains
        a field called `command` which identifies what the message should achieve.

        As a reaction to a received message, we can for example do the following:

        * create a new state machine instance to handle the incoming messages,
        * route the message to an existing state machine session,
        * handle the message right here,
        * throw the message away.

        """
        self._logger.debug('Incoming message to topic {}'.format(msg.topic))

        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception as err:
            self._logger.error('Message sent to topic {} had no valid JSON. Message ignored. {}'.format(msg.topic, err))
            return
        command = payload.get('command')
        name = payload.get('name')
        duration = payload.get('duration')

        print(payload)
        if (command == "new_timer"):
            print(name)
            timer_stm = TimerLogic(name, duration, self)
            self.stms.append(name)

        if (command == "status_all_timers"):
            print('all_timers')
            for id in self.stms:
                self.stm_driver.send('report', id)

        if (command == "status_single_timer"):
            print('timer')
            self.stm_driver.send('report', name)

    def __init__(self):
        """
        Start the component.

        ## Start of MQTT
        We subscribe to the topic(s) the component listens to.
        The client is available as variable `self.client` so that subscriptions
        may also be changed over time if necessary.

        The MQTT client reconnects in case of failures.

        ## State Machine driver
        We create a single state machine driver for STMPY. This should fit
        for most components. The driver is available from the variable
        `self.driver`. You can use it to send signals into specific state
        machines, for instance.

        """
        # get the logger object for the component
        self._logger = logging.getLogger(__name__)
        print('logging under name {}.'.format(__name__))
        self._logger.info('Starting Component')

        # create a new MQTT client
        self._logger.debug('Connecting to MQTT broker {} at port {}'.format(MQTT_BROKER, MQTT_PORT))
        self.mqtt_client = mqtt.Client()
        # callback methods
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        # subscribe to proper topic(s) of your choice
        self.mqtt_client.subscribe(MQTT_TOPIC_INPUT)
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()

        # we start the stmpy driver, without any state machines for now
        self.stm_driver = stmpy.Driver()
        self.stm_driver.start(keep_active=True)
        self._logger.debug('Component initialization finished')

        self.stms = []
        self.create_gui()

    def create_gui(self):
        self.app = gui()
        self.app.addLabel("title", " HospiTalkie ")

        self.app.setLabelBg("title", "orange")

        def extract_timer_name(label):
            label = label.lower()
            if 'spaghetti' in label: return 'spaghetti'
            if 'green tea' in label: return 'green tea'
            if 'soft eggs' in label: return 'soft eggs'
            return None

        def extract_duration_seconds(label):
            label = label.lower()
            if 'spaghetti' in label: return 600
            if 'green tea' in label: return 120
            if 'soft eggs' in label: return 240
            return None

        def publish_command(command):
            payload = json.dumps(command)
            self._logger.info(command)
            self.mqtt_client.publish(MQTT_TOPIC_INPUT, payload=payload, qos=2)

        self.app.startLabelFrame('Buttons:')

        def on_button_pressed_start(title):
            name = extract_timer_name(title)
            duration = extract_duration_seconds(title)
            command = {"command": "new_timer", "name": name, "duration": duration}
            publish_command(command)

        self.app.addButton('Go buttion', on_button_pressed_start)
        self.app.addButton('Back button', on_button_pressed_start)
        self.app.addButton('Scroll', on_button_pressed_start)
        self.app.stopLabelFrame()

        self.app.startLabelFrame('Display:')
        self.app.addLabel("output", "Display", 0, 0)
        self.app.stopLabelFrame()


        self.app.go()

    def stop(self):
        """
        Stop the component.
        """
        # stop the MQTT client
        self.mqtt_client.loop_stop()

        # stop the state machine Driver
        self.stm_driver.stop()


# logging.DEBUG: Most fine-grained logging, printing everything
# logging.INFO:  Only the most important informational log items
# logging.WARN:  Show only warnings and errors.
# logging.ERROR: Show only error messages.

debug_level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(debug_level)
ch = logging.StreamHandler()
ch.setLevel(debug_level)
formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

t = TimerManagerComponent()