from mqtt_client import MQTTClient
from login_gui import LoginGui

class HospiTalkie:
    """
    State Machine for a named HospiTalkie

    TODO: Only include logic for functions defined by the statemachine.

    """
    def start(self, stm_driver):
        #TODO: get the name of the "person"
        print("init HospiTalkie")
        self.name = "Ola"
        self.stm_driver = stm_driver
        self.mqtt_client = MQTTClient(self.name, self.stm_driver)
        self.login_gui = LoginGui(self.stm_driver)

    def setRecipient(self, topic):
        print("setRecipient HospiTalkie")
        #maybe need to convert topic from json if not done in GUI
        self.currentRecipient = topic

    def sendMessage(self, message):
        print("sendMessage HospiTalkie")
        msg = json.dumps({"message": message, "from": name})
        
        self.mqtt_client.publish(self.currentRecipient, msg)

    def authenticate(self, usr, pwd):
        print("authenticate HospiTalkie")
        self.mqtt_client.start_client(usr, pwd)

    def loginSuccess(self):
        print("loginSuccess HospiTalkie")
        print(type(self))
        dir(self)

    def loginError(self):
        print("loginError HospiTalkie")
        self.login_gui.login_error()
        
    def loadPhoneBook(self):
        print("loadPhoneBook")

    def display(self, text):
        print("Displaying: " + text)

    def mute(self):
        print("mute")

    def unmute(self):
        print("unmute")

    def highlightNextMessage(self):
        print("highlightNextMessage")
        
    def storeMessage(self):
        print("storeMessage")

    def startRecording(self):
        print("Start Recording")

    def stopRecording(self):
        print("Stop Recording")
        
    #TODO: implement all functions defined in the state machine