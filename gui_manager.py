from appJar import gui
import paho.mqtt.client as mqtt
import stmpy
import logging
from threading import Thread
import json

"call funtion with: self.create_gui()"

message_received = False

def create_gui(self):
    self.app = gui("HospiTalkie", "300x500")
    self.app.setFont(16)
    self.app.setBg("lightGrey")

    self.app.addLabel("title", " HospiTalkie ")
    self.app.setLabelBg("title", "orange")


    def extract_button(label):
        label = label.lower()
        if 'go' in label: return 'go'
        if 'back' in label: return 'back'
        if 'scroll' in label: return 'scroll'
        return None

    "logic in stm"
    def on_button_pressed(title):
        button = extract_button(title)
        return button
        print("pressed")

    self.app.setInPadding([10, 10])
    self.app.addButton('Go ', on_button_pressed)
    self.app.addButton('Back ', on_button_pressed)
    self.app.addButton('Scroll ', on_button_pressed)

    self.app.addHorizontalSeparator(4, 0, 4, colour="white")
    self.app.addMessage("mess", """This is the dislapy field.""")

    "implement function"
    if message_received:
        app.yesNoBox("messread", "Du har en melding. Vil du lese?", parent=None)
        app.setMessage("mess", """You received a message""")

    self.app.go()

"self.create_gui()"

