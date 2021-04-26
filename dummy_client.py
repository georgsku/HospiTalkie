import paho.mqtt.client as mqtt

MQTT_BROKER = '78.156.8.124'
MQTT_PORT = 1883
name = "Trond"
MQTT_TOPIC_HOSPITALKIE = 'ttm4115/team_3/hospitalkie'
MQTT_STATUS = 'status/'
MQTT_PHONEBOOK = 'phonebook/'

class dummyClient:
    """Manages all MQTT functionallity"""
    def __init__(self):
        #create new mqtt client
        self.client = mqtt.Client()

        #callback methods
        self.client.on_message = self.on_message

        self.client.will_set(MQTT_STATUS,0, qos=0, retain=True) 

        # Connect to the broker
        self.client.username_pw_set(username="teamtree", password="teamtree")
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        
        self.client.subscribe("teamtree/" + name)
        self.client.subscribe("phonebook/" + name)

        
        # start the internal loop to process MQTT messages
        self.client.loop_forever()
        client.publish(MQTT_STATUS + name, 1, qos=0, retain=True)
        client.publish(MQTT_PHONEBOOK + name, "getPhonebook", qos=0, retain=True)

    def on_message(self, client, userdata, msg):
        if msg.topic == MQTT_PHONEBOOK + name:
            phonebook = str(msg.payload.decode("utf-8"))
            print(phonebook)
        else:
            message = str(msg.payload.decode("utf-8"))
            print(message)

    def on_connect(client, userdata, flags):
        client.publish(MQTT_STATUS + name, 1, qos=0, retain=True)
        client.publish(MQTT_PHONEBOOK + name, "getPhonebook", qos=0, retain=True)
        print("hei")

  
dummyclient = dummyClient()