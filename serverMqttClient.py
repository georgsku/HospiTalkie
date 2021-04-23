import paho.mqtt.client as mqtt

MQTT_BROKER = '78.156.8.124'
MQTT_PORT = 1883

MQTT_TOPIC_HOSPITALKIE = 'ttm4115/team_3/hospitalkie'
MQTT_STATUS = 'status/'

class serverMQTTClient:
    """Manages all MQTT functionallity"""
    def __init__(self):
        #create new mqtt client
        self.client = mqtt.Client()

        #callback methods
        self.client.on_message = self.on_message

        # Connect to the broker
        self.client.connect(MQTT_BROKER, MQTT_PORT)

        # Subscribe status topic
        self.client.subscribe(MQTT_STATUS + "#")
        
        # start the internal loop to process MQTT messages
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception as err:
            self._logger.error('Message sent to topic {} had no valid JSON. Message ignored. {}'.format(msg.topic, err))
            return
        command = payload.get('command')
        name = payload.get('name')
        #something

  
server = serverMQTTClient()