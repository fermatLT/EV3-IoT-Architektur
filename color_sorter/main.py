#!/usr/bin/env pybricks-micropython

"""
This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

"""
import os
import sys
import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.media.ev3dev import Font
from pybricks.tools import wait
from umqtt.robust import MQTTClient
from  mindsensorsPYB import PPS58
from  mindsensorsPYB import EV3Matrix
from  mindsensorsPYB import DIST_ToF
from  mindsensorsPYB import EV3RFid
from  mindsensorsPYB import LINELEADER
from  mindsensorsPYB import TFTPACK
from  mindsensorsPYB import ABSIMU
from  mindsensorsPYB import IRThermometer
from  mindsensorsPYB import VOLT
from  mindsensorsPYB import PFMATE
from  mindsensorsPYB import SUMOEYES

from time import  strftime


# Init a new EV3 Brick
ev3 = EV3Brick()

# Init  RFID Reader 
rfid= EV3RFid(Port.S4,0x22)
rfid_list = [694788313, 5036027]

# Setup connection to broker
MQTT_ClientID = "EV3"

"MQTT_Broker IP must be the one from the EV3 or the Raspberry Pi, depending from the setup"
#IP Raspberry Pi
#MQTT_Broker = "192.168.2.123"

#IP LEGO Ev3
MQTT_Broker = "192.168.2.73"

# Publish data and messages to topic
MQTT_Topic_Status = "/home/status"
MQTT_Topic_Programm = "/home/programm"
MQTT_Topic_Meldungen = "/home/meldungen"
MQTT_Topic_Meldungen_Reset = "/home/meldungen/reset"


# Incoming Messages Function
def getmessages(topic, msg):
    if topic == MQTT_Topic_Status.encode():
        ev3.screen.print(str(msg.decode()))


client = MQTTClient(MQTT_ClientID, MQTT_Broker)
client.connect()

client.set_callback(getmessages)
client.subscribe(MQTT_Topic_Status)
client.subscribe(MQTT_Topic_Meldungen_Reset)
client.publish(MQTT_Topic_Status,'Online')
client.publish(MQTT_Topic_Programm,'Start')


# Font size
font_size = Font(size=18)
ev3.speaker.set_speech_options("de", "m2", 140)

while True:
    client.check_msg()
    time.sleep(0.1)
    break

# Initialize the motors that drive the conveyor belt and eject the objects
ev3.screen.draw_text(30,50, "Initialisieren...")
belt_motor = Motor(Port.D)
feed_motor = Motor(Port.A)

# Initialize the Touch Sensor
touch_sensor = TouchSensor(Port.S1)
touch_sensor_two = TouchSensor(Port.S3)

# Initialize the Color Sensor. It is used to detect the color of the objects.
color_sensor = ColorSensor(Port.S2)
#color_sensor_two = ColorSensor(Port.S3)

feed_motor.run_until_stalled(150)
feed_motor.run_angle(450, -180)


belt_motor.run(-500)
while not touch_sensor.pressed():
    pass
belt_motor.stop()
wait(1000)
belt_motor.reset_angle(0)

ev3.screen.clear()
ev3.screen.draw_text(5,50, "Lade den Schaft")
ev3.speaker.say("Lade den Schaft")

wait(5000)
ev3.screen.clear()
ev3.screen.set_font(font_size)
ev3.screen.draw_text(0,50,"Starte das Programm")
ev3.speaker.say("Starte das Programm indem du die Pfeiltaste nach unten drückst")

while True:

    rfid.clearUID()
    print(rfid.GetFirmwareVersion())
    print(rfid.GetDeviceId())
    print(rfid.readUID())

    pressed = Button.DOWN in ev3.buttons.pressed()

    if pressed:
        client.publish(MQTT_Topic_Programm, 'Farbsortierer')
        ev3.speaker.beep()
        ev3.light.on(Color.GREEN)
        wait(2000)
        ev3.screen.clear()
        ev3.screen.load_image(ImageFile.EV3_ICON)

        def eject():
            feed_motor.run_angle(1500, 90)
            feed_motor.run_angle(1500, -90)

        def breakdown():
            ev3.speaker.beep()
            client.publish(MQTT_Topic_Status, 'Fehler')
            """
            Send Notification to Node-Red Server
            Warning, Error occured
            """
            client.subscribe(MQTT_Topic_Meldungen)
            client.subscribe(MQTT_Topic_Meldungen_Reset)
            client.publish(MQTT_Topic_Meldungen, 'Fehlercode EC578')

            while True:
                
                ev3.light.on(Color.RED)
                rfid_check = rfid.readUID()
                
                ev3.screen.load_image(ImageFile.WARNING)
                
                # Condition for RFID Authorization, RFID UI 694788313
                if rfid_check in rfid_list:
                    client.publish(MQTT_Topic_Status, 'Service')
                    ev3.speaker.beep()
                    ev3.screen.clear()
                    
                    while True:
                        left_pressed = Button.LEFT in ev3.buttons.pressed()
                        wait(1000)
                        ev3.screen.draw_text(30,50, "Service Mode")

                        """
                        Send Notification to Node-Red Server
                        Machine in Service Mode
                        API GET request to CDN
                        """

                        if left_pressed:
                            client.publish(MQTT_Topic_Status,'Online')
                            ev3.screen.clear()
                            rfid.clearUID()
                            ev3.screen.load_image(ImageFile.EV3_ICON)
                            wait(2000)
                            break
                            
                            """
                            Send Notification to Node-Red Server
                            Machine in Standard Mode
                            """
                    break

        while True:
            color = color_sensor.color()
            ev3.light.on(Color.GREEN)

            # Simulation of breakdown
            if touch_sensor_two.pressed():
                breakdown()

            elif color == Color.BLUE:
                client.publish(MQTT_Topic_Programm,'Blue')   
                ev3.speaker.say("Blau")
                belt_motor.run_target(500, 5)
                eject()
                wait(1000)

            elif color == Color.GREEN: 
                client.publish(MQTT_Topic_Programm,'Green')
                ev3.speaker.say("Grün")
                belt_motor.run_target(500, 140)
                eject()
                wait(1000)

            elif color == Color.YELLOW:
                client.publish(MQTT_Topic_Programm,'Yellow')
                ev3.speaker.say("Gelb")
                belt_motor.run_target(500, 357)
                eject()
                wait(1000)

            elif color == Color.RED:   
                client.publish(MQTT_Topic_Programm,'Red')
                ev3.speaker.say("Rot")
                belt_motor.run_target(500, 530)
                eject()
                wait(1000)
