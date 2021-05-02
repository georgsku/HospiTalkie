import paho.mqtt.client as mqtt
import json
import string

MQTT_BROKER = '78.156.8.124'
MQTT_PORT = 1883

MQTT_TOPIC_HOSPITALKIE = 'hospitalkie/'
MQTT_STATUS = 'status/'
MQTT_PHONEBOOK = 'phonebook/'

phonebook = {"All": "", "George": "george", "Julie": "Julie", "Trond": "Trond", "Anjan": "Anjan"}




class serverMQTTClient:
    """Manages all MQTT functionallity"""
    def __init__(self):
        #create new mqtt client
        self.client = mqtt.Client()

        #callback methods
        self.client.on_message = self.on_message
        
        self.client.username_pw_set(username="ola", password="123")

        # Connect to the broker
        self.client.connect(MQTT_BROKER, MQTT_PORT)

        # Subscribe status topic
        self.client.subscribe(MQTT_STATUS + "#")
        self.client.subscribe(MQTT_PHONEBOOK + "#")
        
        # start the internal loop to process MQTT messages
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):

        def send_phonebook():
            for name in phonebook:
                client.publish(MQTT_PHONEBOOK + phonebook[name], json.dumps(phonebook), qos=0, retain=True)      

        message = str(msg.payload.decode("utf-8"))
        topic = msg.topic.split("/")[0]
        name = msg.topic.split("/")[1]
        print("message received " , message , ": " + topic, ": " + name)
        if topic == "status":
            if message == "1":
                phonebook[name.title()] = name
                send_phonebook()
                print("Updated phonebook by appending: ", phonebook)
            elif message == "0":
                if phonebook.get(name.title()):
                    phonebook.pop(name.title())
                    send_phonebook()
                    print("Updated phonebook by removing: ", phonebook)
        elif topic == "phonebook":
            if message == "getPhonebook":
                print("Sending phonebook to: ", name)
                client.publish(MQTT_PHONEBOOK + name, json.dumps(phonebook), qos=0, retain=True)        
        
    
  

  
server = serverMQTTClient()