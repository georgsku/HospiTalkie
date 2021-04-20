from appJar import gui
import paho.mqtt.client as mqtt
import stmpy
import logging
from threading import Thread
import json

"call funtion with: self.create_gui()"

message_received = False

def create_gui():
    app = gui("HospiTalkie", "300x500")
    app.setFont(16)
    app.setBg("lightGrey")

    app.addLabel("title", " HospiTalkie ")
    app.setLabelBg("title", "orange")


    def extract_button(label):
        label = label.lower()
        if 'go' in label: return 'go'
        if 'back' in label: return 'back'
        if 'scroll' in label: return 'scroll'
        return None

    "logic in stm"
    def on_button_pressed():
        print("pressed")

    app.setInPadding([10, 10])
    app.addButton('Go ', on_button_pressed)
    app.addButton('Back ', on_button_pressed)
    app.addButton('Scroll ', on_button_pressed)

    app.addHorizontalSeparator(4, 0, 4, colour="white")
    app.addMessage("mess", """This is the dislapy field.""")
    if message_received:
        app.yesNoBox("messread", "Du har en melding. Vil du lese?", parent=None)
        app.setMessage("mess", """You received a message""")

    app.go()

create_gui()

