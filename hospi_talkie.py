from mqtt_client import MQTTClient
from login_gui import LoginGui
from strings import get_string
from audio.recorder import Recorder
from audio.player import Player
from audio.file_manager import FileManager
import glob
import re
import datetime
import time


""" import logging
debug_level = logging.DEBUG
logger = logging.getLogger('stmpy')
logger.setLevel(debug_level)
ch = logging.StreamHandler()
ch.setLevel(debug_level)
formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch) """

class HospiTalkie:
    """
    State Machine for a named HospiTalkie

    TODO: Only include logic for functions defined by the statemachine.

    """
    def start(self, stm_driver, login_gui):
        print("init HospiTalkie")
        self.name = "Ola"
        self.stm_driver = stm_driver
        self.login_gui = login_gui
        self.mqtt_client = MQTTClient(self.name, self.stm_driver)
        self.player = Player(self.stm_driver)
        self.recorder = Recorder(self.stm_driver)
        self.fileManager = FileManager(self.stm_driver)
        self.messageCounter = 0
        self.isBuffer = True
        self.sender = None
        

    def setRecipient(self):
        print("setRecipient HospiTalkie")
        self.currentRecipient = self.mqtt_client.selected_recipient
        self.currentRecipientTopic = self.mqtt_client.phonebook[self.currentRecipient.title()].lower()
        print(self.currentRecipient, self.currentRecipientTopic)

    def sendMessage(self, message):
        print("sendMessage HospiTalkie")
        print("Sending message to:" , self.currentRecipientTopic)
        self.mqtt_client.publish(self.currentRecipientTopic, message)
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
        print("displaying: " + text)
        if text == "Contacts":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("choose_reciever"))
            prevContact = list(self.mqtt_client.phonebook.keys())[(self.mqtt_client.phonebook_counter - 1) % len(self.mqtt_client.phonebook)]
            self.mqtt_client.selected_recipient = list(self.mqtt_client.phonebook.keys())[self.mqtt_client.phonebook_counter % len(self.mqtt_client.phonebook)]
            nextContact = list(self.mqtt_client.phonebook.keys())[(self.mqtt_client.phonebook_counter + 1) % len(self.mqtt_client.phonebook)]
            print("Displaying: " + self.mqtt_client.selected_recipient)
            contact = prevContact+ "\n" + "--> " + self.mqtt_client.selected_recipient + "\n" + nextContact
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", ""+contact+"")
        elif text == "next_contact":
            self.mqtt_client.phonebook_counter += 1
        elif text == "btn_record":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("record_message"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("btn_record"))
        elif text == "main_screen":
            print("main screen")
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("idle"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("main_screen"))
            self.login_gui.app.setLabel("title", "Welcome To HospiTalkie " + self.mqtt_client.name.title())
        elif text == "new_messages":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("new_message"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("new_messages_description"))
        elif text == "saved_messages":
            self.isBuffer = False
            self.messages = glob.glob("./Messages/*.wav")
            self.message = self.messages[self.messageCounter % len(self.messages)]
            self.currentRecipient = self.message[self.message.rfind("/"):][1:].split("-")[0]
            self.currentRecipientTopic = self.mqtt_client.phonebook[self.currentRecipient]
            self.messageDisplay = re.search('./Messages/(.*).wav', self.message).group(1)
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("saved_messages"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("saved_messages") + "\n" + self.messageDisplay)
        elif text == "reply_message":
            print("Current recipient: " + str(self.sender))

            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("reply"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("reply_message", str(self.sender)))
        elif text == "recording":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("recording"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("recording"))
        elif text == "done_recording":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("done_recording"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("done_recording"))
        elif text == "playing":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("playing"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("playing_from", str(self.sender)))
        elif text == "play_or_store":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("new_message"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("play_or_store"))
        elif text == "next_message":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string("next_message"))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", "message here!")
        elif text == "delete_message":
            self.login_gui.app.queueFunction(self.login_gui.app.setTitle, get_string(""))
            self.login_gui.app.queueFunction(self.login_gui.app.setMessage, "mess", get_string("delete_message"))

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
        self.messageCounter += 1  

    def getMessage(self, message, sender):
        print("Get Message")
        self.isBuffer = True
        self.sender = sender  #This makes audio message available in "playMessage".
        self.message = message  #This makes audio message available in "playMessage".
        self.currentRecipientTopic = self.mqtt_client.phonebook[self.sender.title()]
        

    def storeMessages(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        print("Store message")
        filename = self.sender.title() + "-" + st
        data = self.message
        self.stm_driver.send("saveFile", "fileManager", args=[filename, data]) 

    def deleteMessages(self):
        print("delete message")
        
    def playNotification(self):
        print("Playing notification")
        self.stm_driver.send("start", "player", args=['notification.wav', False, False]) 

    def playMessage(self):
        print("Play message")
        self.stm_driver.send("start", "player", args=[self.message, self.isBuffer, True])

    def startRecording(self):
        print("Start Recording")
        self.stm_driver.send('start', 'recorder')

    def stopRecording(self):
        print("Stop Recording")
        self.stm_driver.send('stop', 'recorder')
        