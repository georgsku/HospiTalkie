from mqtt_client import MQTTClient
from login_gui import LoginGui


class HospiTalkie:
    """
    State Machine for a named HospiTalkie

    TODO: Only include logic for functions defined by the statemachine.

    """
    def start(self, stm_driver, login_gui):
        #TODO: get the name of the "person"
        print("init HospiTalkie")
        self.name = "Ola"
        self.stm_driver = stm_driver
        self.login_gui = login_gui
        self.mqtt_client = MQTTClient(self.name, self.stm_driver)
        

    def setRecipient(self):
        print("setRecipient HospiTalkie")
        #maybe need to convert topic from json if not done in GUI
        self.currentRecipient = self.mqtt_client.selected_recipient
        self.currentRecipientTopic = self.mqtt_client.phonebook[self.currentRecipient]

    def sendMessage(self, message):
        print("sendMessage HospiTalkie")
        msg = json.dumps({"message": message, "from": name})
        
        self.mqtt_client.publish(self.currentRecipient, msg)

    def authenticate(self, usr, pwd):
        print("authenticate HospiTalkie")
        self.mqtt_client.start_client(usr, pwd)

    def loginSuccess(self):
        print("loginSuccess HospiTalkie")
        self.login_gui.switch_gui()
        

    def loginError(self):
        print("loginError HospiTalkie")
        self.login_gui.login_error()
        
    def loadPhoneBook(self):
        print("loadPhoneBook")

    def display(self, text):
        if text == "Contacts":
            self.login_gui.app.setTitle("Choose Reciever")
            prevContact = list(self.mqtt_client.phonebook.keys())[(self.mqtt_client.phonebook_counter - 1) % len(self.mqtt_client.phonebook)]
            self.mqtt_client.selected_recipient = list(self.mqtt_client.phonebook.keys())[self.mqtt_client.phonebook_counter % len(self.mqtt_client.phonebook)]
            nextContact = list(self.mqtt_client.phonebook.keys())[(self.mqtt_client.phonebook_counter + 1) % len(self.mqtt_client.phonebook)]
            print("Displaying: " + self.mqtt_client.selected_recipient)
            contact = prevContact+ "\n" + "--> " + self.mqtt_client.selected_recipient + "\n" + nextContact
            self.login_gui.app.setMessage("mess", ""+contact+"")
        elif text == "next_contact":
            print("heo")
            self.mqtt_client.phonebook_counter += 1
        elif text == "btn_record":
            self.login_gui.app.setTitle("Record Message")
            self.login_gui.app.setMessage("mess", "Press Go to record a message")
        elif text == "main_screen":
            print("main screen")
            self.login_gui.app.setTitle("Idle")
            self.login_gui.app.setMessage("mess", "Welcome, press go btn to enter contacts, or back btn to enter messages")
        elif text == "new_messages":
            self.login_gui.app.setTitle("New Messages")
            self.login_gui.app.setMessage("mess", "You got a new message, would you like to read/hear?")
        elif text == "saved_messages":
            self.login_gui.app.setTitle("Saved Messages")
            self.login_gui.app.setMessage("mess", "Saved Messages")
        elif text == "reply_message":
            self.login_gui.app.setTitle("Reply To Message")
            self.login_gui.app.setMessage("mess", "Press go btn to reply back to idle")
            

    def mute(self):
        print("mute")
        self.login_gui.app.setTitle("Do Not Disturb")
        self.login_gui.app.setButton("Mute", "Unmute")
        self.login_gui.app.setMessage("mess", "You will not be disturbed!")


    def unmute(self):
        print("unmute")
        self.login_gui.app.setButton("Mute", "Mute")
        

    def highlightNextMessage(self):
        print("highlightNextMessage")
        
    def storeMessage(self):
        print("storeMessage")

    def getMessage(self, message):
        print("Get Message")
        self.message = message

    def storeMessages(self):
        print("Store message")

    def playMessage(self):
        print("Play message")
        self.login_gui.app.setMessage("mess", self.message)

    def startRecording(self):
        print("Start Recording")

    def stopRecording(self):
        print("Stop Recording")
        
    #TODO: implement all functions defined in the state machine