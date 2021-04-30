from mqtt_client import MQTTClient
from login_gui import LoginGui
from strings import get_string
from audio.recorder import Recorder
from audio.player import Player

"""
import logging
debug_level = logging.DEBUG
logger = logging.getLogger('stmpy')
logger.setLevel(debug_level)
ch = logging.StreamHandler()
ch.setLevel(debug_level)
formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
"""
class HospiTalkie:
    """
    State Machine for a named HospiTalkie

    TODO: Only include logic for functions defined by the statemachine.

    """
    def start(self, stm_driver, login_gui):
        #TODO: get the name of the "person"
        print("init HospiTalkie")
        self.name = "Andre2"
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
        
        #TODO: Check this!! the audio data cant be json encoded.... but we still need the sender
        #msg = json.dumps({"message": message, "from": name}) 
        
        print("message")
        print(len(message))
        self.mqtt_client.publish(self.currentRecipient, message)
        self.stm_driver.send("messagePublished", "HospiTalkie") # TODO: Use callback instead then send??

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
        import threading
        print("thread: ")
        print(threading.current_thread())
        if text == "Contacts":

            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("choose_reciever"))
            prevContact = list(self.mqtt_client.phonebook.keys())[(self.mqtt_client.phonebook_counter - 1) % len(self.mqtt_client.phonebook)]
            self.mqtt_client.selected_recipient = list(self.mqtt_client.phonebook.keys())[self.mqtt_client.phonebook_counter % len(self.mqtt_client.phonebook)]
            nextContact = list(self.mqtt_client.phonebook.keys())[(self.mqtt_client.phonebook_counter + 1) % len(self.mqtt_client.phonebook)]
            print("Displaying: " + self.mqtt_client.selected_recipient)
            contact = prevContact+ "\n" + "--> " + self.mqtt_client.selected_recipient + "\n" + nextContact
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", ""+contact+"")
        elif text == "next_contact":
            print("heo")
            self.mqtt_client.phonebook_counter += 1
        elif text == "btn_record":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("record_message"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("btn_record"))
        elif text == "main_screen":

            print("main screen")
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("idle"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("main_screen"))
        elif text == "new_messages":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("new_message"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("new_messages_description"))
        elif text == "saved_messages":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("saved_messages"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("saved_messages"))
        elif text == "reply_message":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("reply_message"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("reply_messaged"))
        elif text == "done_recording":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("done_recording"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("done_recording"))

    def mute(self):
        print("mute")
        self.login_gui.app.setTitle(get_string("dont_disturb"))
        self.login_gui.app.queueFunction(self.login_gui.app.setButton, "Mute", get_string("unmute"))
        self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("not_disturbed"))

    def unmute(self):
        print("unmute")
        self.login_gui.app.queueFunction(self.login_gui.app.setButton, "Mute", get_string("mute"))
        

    def highlightNextMessage(self):
        print("highlightNextMessage")
        
    def storeMessage(self):
        print("storeMessage")

        #TODO: finish audiomanager for saving and deleting files...
        #Can we just keep everything in memory??? => Easy...
        #audiomanager = AudioManager(self.stm_driver)
        #self.stm_driver.send("save", "AudioManager")

    def getMessage(self, message):
        print("Get Message")
        self.message = message  #This makes audio message available in "playMessage".
        # TODO: save or keep voiceee message in memory?
        

    def storeMessages(self):
        print("Store message")

    def playMessage(self):
        print("Play message")
        self.player = Player(self.stm_driver)
        self.stm_driver.send("start", "player", args=[self.message]) #Getting error because of playing in-memory bufferr....
        # TODO: find a way to detect if json.... if just text and not audio..
        #self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", self.message)

    def startRecording(self):
        print("Create recorder")
        self.recorder = Recorder(self.stm_driver)
        print("Start Recording")
        self.stm_driver.send('start', 'recorder')

    def stopRecording(self):
        print("Stop Recording")
        self.stm_driver.send('stop', 'recorder')
        
    #TODO: implement all functions defined in the state machine