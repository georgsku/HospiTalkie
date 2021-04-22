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


class HospiTalkie:
    """
    State Machine for a named HospiTalkie
    """
    
    def on_message(self, client, userdata, msg):
            try:
                payload = json.loads(msg.payload.decode("utf-8"))
            except Exception as err:
                self._logger.error('Message sent to topic {} had no valid JSON. Message ignored. {}'.format(msg.topic, err))
                return
            command = payload.get('command')
            name = payload.get('name')
            #something

    def __init__(self, name, component):
        
        #create new mqtt client
        self.mqtt_client = mqtt.Client()
        
        #callback methods
        self.mqtt_client.on_message = self.on_message
        
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

        # subscribe to own topic
        self.ownTopic = MQTT_TOPIC_HOSPITALKIE + '/' + name
        self.mqtt_client.subscribe(self.ownTopic)

        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()
        
        self.name = name
        self.component = component
        self.currentRecipient = None

        def setRecipient(topic):
            #maybe need to convert topic from json if not done in GUI
            self.currentRecipient = topic

        def sendMessage(message):
            #maybe need to convert message to json if not done in GUI
            self.component.mqtt_client.publish(self.currentRecipient, message)


        # the transitions
      
        
        # the states:
        


        
        


class HospiTalkieManager:
    """
    The component to manage named HospiTalkies.
    
    Does 4 things:

        1. Creates a driver when initialized
        2. Creates new a new HospiTalkie instance when receiving a certain message
        3. Holds list over connected HospiTalkies
        4. Removes HospiTalkie from list and broadcasts that a HospiTalkie is disconnected (could be done with last-will another place?)


    """

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))
        
        

    def on_message(self, client, userdata, msg):
                
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception as err:
            self._logger.error('Message sent to topic {} had no valid JSON. Message ignored. {}'.format(msg.topic, err))
            return

        #Formatted in the GUI(?) like the timerManager stuff
        command = payload.get('command')
        name = payload.get('name')
        
        print(payload)
        if (command == "new_client"):
            hospiTalkie = HospiTalkie(name, self)
            #This probably should be done with IDs instead of "name". Atleast "name" should be unique
            self.stms.append(name)


        # Possibility of doing disconnections: This manager receives message with command "disconnect" and name
        # the HospiTalkie is removed from list of HospiTalkies and "disconnection" is sent to all HospiTalkies
        # this should trigger a function in each HospiTalkie which triggers the updatePhonebook function
        # this probably won't work :)
        
        if (command == "disconnect"):
            self.stms.remove(name)
            self.component.mqtt_client.publish("disconnection")



    def __init__(self):
 
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


t = ClientManagerComponent()
