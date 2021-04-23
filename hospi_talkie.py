import MQTTClient

class HospiTalkie:
    """
    State Machine for a named HospiTalkie

    TODO: Only include logic for functions defined by the statemachine.

    """
    def init(self):
        #TODO: get the name of the "person"
        self.name = "Ola"
        self.mqtt_client = MQTTClient(self.name, self.stm_driver)

    def setRecipient(topic):
        #maybe need to convert topic from json if not done in GUI
        self.currentRecipient = topic

    def sendMessage(message):
        #maybe need to convert message to json if not done in GUI
        self.mqtt_client.publish(self.currentRecipient, message)

    def authenticate():

    def getPhoneBook():

    def loadPhoneBook():
          
    def display():

    def mute():

    def unmute():

    def highlightNextMessage():

    def storeMessage():

    def startRecording():

    def stopRecording():
    
        
    #TODO: implement all functions defined in the state machine