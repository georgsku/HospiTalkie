import paho.mqtt.client as mqtt
import stmpy
import logging
from threading import Thread
import json
from appJar import gui

MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883


MQTT_TOPIC_HOSPITALKIE = 'ttm4115/team_3/hospitalkie'
MQTT_TOPIC_INPUT = 'ttm4115/team_3/hospitalkie/input'
MQTT_TOPIC_PHONEBOOK = 'ttm4115/team_3/phonebook'


class ClientLogic:
    """
    State Machine for a named HospiTalkie
    """
    def __init__(self, name, component):
        self._logger = logging.getLogger(__name__)
        self.name = name
        self.component = component
        self.ownTopic = MQTT_TOPIC_HOSPITALKIE + '/' + name
        self.component.mqtt_client.subscribe(self.ownTopic)
        self.phoneBook = getPhonebook()

        def getPhonebook():
            return self.component.stm_driver.stms


        def setRecipient(topic):
            #maybe need to convert topic to topic format

            self.currentRecipient = topic

        def sendMessage(message):
            #maybe need to convert message to json 

            self.component.mqtt_client.publish(self.currentRecipient, message)


        # the transitions
      
        
        # the states:
        

        self.stm = stmpy.Machine(name=self.name, transitions=[t0, t1, t2], obj=self, states=[active, completed])
        self.component.stm_driver.add_machine(self.stm)

        
        


class ClientManagerComponent:
    """
    The component to manage named HospiTalkies.

    This component connects to an MQTT broker and listens to commands.
    To interact with the component, do the following:

    * Connect to the same broker as the component.

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
        
        print(payload)
        if (command == "new_client"):
            hospiTalkie = ClientLogic(name, self)
            self.stms.append(name)


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

        # subscribe to input topic
        self.mqtt_client.subscribe(MQTT_TOPIC_INPUT)

        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()

        # we start the stmpy driver, without any state machines for now
        self.stm_driver = stmpy.Driver()
        self.stm_driver.start(keep_active=True)
        self._logger.debug('Component initialization finished')
        
        self.stms = []
        self.create_gui()
    
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


t = ClientManagerComponent()