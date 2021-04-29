from appJar import gui
import paho.mqtt.client as mqtt
import stmpy
import logging
from threading import Thread
import json

"call funtion with: self.create_gui()"
class GuiManager():
    

    def __init__(self):
        print("init GuiManager")
        
        app = gui("HospiTalkie", "300x500")
        app.setFont(16)
        app.setBg("lightGrey")

        app.addLabel("title", " HospiTalkie ")
        app.setLabelBg("title", "orange")
        app.setInPadding([10, 10])
        app.addButton('Go ', on_button_pressed)
        app.addButton('Back ', on_button_pressed)
        app.addButton('Scroll ', on_button_pressed)

        app.addHorizontalSeparator(4, 0, 4, colour="white")
        app.addMessage("mess", """This is the dislapy field.""")

        app.go()

    def extract_button(label):
        label = label.lower()
        if 'go' in label: return 'goBtnPressed'
        if 'back' in label: return 'backBtnPressed'
        if 'scroll' in label: return 'scrollBtnScrolled'
        return None

    "logic in stm"
    def on_button_pressed(title):
        button = extract_button(title)

        "send which button is pressed to the state machine"
        self.stm_driver.send(button)
        return button

    "implement function in hospietalkie and call when incoming message arrives" 
    def message_received(message):
        self.app.yesNoBox("messread", "Du har en melding. Vil du lese?", parent=None)
        self.app.setMessage("mess", ""+message+"")
        

