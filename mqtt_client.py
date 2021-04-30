import paho.mqtt.client as mqtt
import json

MQTT_BROKER = '78.156.8.124'
MQTT_PORT = 1883

MQTT_TOPIC_HOSPITALKIE = 'hospitalkie'
MQTT_TOPIC_INPUT = 'input'
MQTT_PHONEBOOK = 'phonebook/'
MQTT_STATUS = 'status/'

class MQTTClient:
    """Manages all MQTT functionallity"""
    def __init__(self, name, stm_driver):
        print("init MqttClient")
        self.name = name
        self.stm_driver = stm_driver
        self.phonebook = {"George": "george", "Julie": "Julie", "Trond": "Trond", "Anjan": "Anjan"}
        self.phonebook_counter = 0
        self.selected_recipient = None

        #create new mqtt client
        self.mqtt_client = mqtt.Client()

        #callback methods
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
    
        # Set will
        self.mqtt_client.will_set(MQTT_STATUS,0, qos=0, retain=True) 

    def start_client(self, usr, pwd):
        print(usr)
        print(pwd)
        # Connect to the broker
        self.mqtt_client.username_pw_set(username=usr, password=pwd)
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

        # Subscribe to own topic
        self.ownTopic = MQTT_TOPIC_HOSPITALKIE + '/' + self.name
        self.mqtt_client.subscribe(self.ownTopic)
        self.mqtt_client.subscribe("teamtree/" + self.name)
        self.mqtt_client.subscribe("phonebook/" + self.name)
        
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()


    def on_message(self, client, userdata, msg):
        print("Got a new message")
        if msg.topic == MQTT_PHONEBOOK + self.name:
            try:
                message = msg.payload.decode("utf-8")
                message = message.replace("\'", "\"")
                self.phonebook = json.loads(message)
                print("Phonebook: " , self.phonebook)
            except:
                print("wops")
        else:
            #message = str(msg.payload.decode("utf-8"))
            message = msg.payload #Audio in binary
            print("OMG IT WORKS")
            self.stm_driver.send("messageReceived", "HospiTalkie", args=[message])
            #TODO: Need to know who the sender was.....


    def on_connect(self, client, userdata, flags, rc):
        print(rc)
        if rc == 0:
            self.stm_driver.send("loginSuccess", "HospiTalkie")
            client.publish(MQTT_STATUS + self.name, 1, qos=0, retain=True)
            client.publish(MQTT_PHONEBOOK + self.name, "getPhonebook", qos=0, retain=True)
        elif rc == 4:
            self.mqtt_client.loop_stop()
            self.stm_driver.send("loginError", "HospiTalkie")


    def publish(self, recipient, message):
        reciever = MQTT_TOPIC_HOSPITALKIE + '/' + recipient
        self.mqtt_client.publish(reciever, message)
          
    def on_disconnect(self, client, userdata, flags):
        client.publish(MQTT_STATUS + self.name, 0, qos=0, retain=True)

  