from appJar import gui
import paho.mqtt.client as mqtt
import stmpy
import logging
from threading import Thread
import json

"call funtion with: self.create_gui()"

MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

MQTT_TOPIC_HOSPITALKIE = 'ttm4115/team_3/hospitalkie'
MQTT_TOPIC_INPUT = 'ttm4115/team_3/hospitalkie/input'
MQTT_TOPIC_PHONEBOOK = 'ttm4115/team_3/phonebook'

def create_gui():
    app = gui("HospiTalkie", "400x200")

    app.addLabel("title", " HospiTalkie ")
    app.setLabelBg("title", "orange")

    def on_button_pressed():
        print("pressed")

    app.addButton('Go button', on_button_pressed)
    app.addButton('Back button', on_button_pressed)
    app.addButton('Scroll button', on_button_pressed)

    app.go()

create_gui()