#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Color Sorter Program
--------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

"""

from pybricks.hubs import EV3Brick
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
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

import time
import os
import sys


# Init a new EV3 Brick
ev3 = EV3Brick()

# Init  RFID Reader 
rfid= EV3RFid(Port.S4,0x22)


"""
Possible UID RFID Tags
694788313
5036027

"""

# Setup connection to broker
MQTT_ClientID = "EV3"
MQTT_Broker = "192.168.2.73"

"MQTT_Broker IP must be the one from the EV3 or the Raspberry Pi, depending from your setup"

# Publish data and messages to topic
MQTT_Topic_Status = "/home/data"

"""
def getmessages(topic, msg):
    if topic == MQTT_Topic_Status.encode():
        brick.display.text(str(msg.decode()))


client = MQTTClient(MQTT_ClientID, MQTT_Broker)
client.connect()

client.publish(MQTT_Topic_Status, MQTT_ClientID + ' Started')
client.set_callback(getmessages)
client.subscribe(MQTT_Topic_Status)
client.publish(MQTT_Topic_Status, MQTT_ClientID + ' Listening')
"""

while True:
    #client.check_msg()
    time.sleep(0.1)
    break

# Initialize the motors that drive the conveyor belt and eject the objects
ev3.screen.draw_text(30,50, "Initializing...")
belt_motor = Motor(Port.D)
feed_motor = Motor(Port.A)

# Initialize the Touch Sensor. It is used to detect when the belt motor has
# moved the sorter module all the way to the left.
touch_sensor = TouchSensor(Port.S1)
touch_sensor_two = TouchSensor(Port.S3)

# Initialize the Color Sensor. It is used to detect the color of the objects.
color_sensor = ColorSensor(Port.S2)  

feed_motor.run_until_stalled(150)
feed_motor.run_angle(450, -180)


belt_motor.run(-500)
while not touch_sensor.pressed():
    pass
belt_motor.stop()
wait(1000)
belt_motor.reset_angle(0)


brick.display.clear()

ev3.screen.draw_text(5,50, "Load the machine")

wait(5000)
brick.display.clear()

while True:

    rfid.clearUID()
    
    print(rfid.GetFirmwareVersion())
    print(rfid.GetDeviceId())
    print(rfid.readUID())

    pressed = Button.DOWN in brick.buttons()
    ev3.screen.draw_text(30,50, "Start Program")

    if pressed:

        brick.sound.beep(1000, 100, 100)
        ev3.light.on(Color.GREEN)
        wait(2000)
        brick.display.clear()
        ev3.screen.load_image(ImageFile.EV3_ICON)

        def eject():
            feed_motor.run_angle(1500, 90)
            feed_motor.run_angle(1500, -90)

        while not touch_sensor_two.pressed():

            # Wait for 1 second between each sorting action.
            wait(1000)
            color = color_sensor.color()
            ev3.light.on(Color.GREEN)

            # Simulation of breakdown
            if touch_sensor_two.pressed():
                brick.sound.beep(1000, 100, 100)

                """
                Send Notification to Node-Red Server
                Warning, Error occured
                """

                while True:
                    
                    ev3.light.on(Color.RED)
                    rfid_check = rfid.readUID()
                    
                    ev3.screen.load_image(ImageFile.WARNING)
                    
                    # Condition for RFID Authorization
                    if rfid_check == 694788313 :
                        brick.sound.beep(1000, 100, 100)
                        brick.display.clear()
                        
                        while True:
                            second_pressed = Button.LEFT in brick.buttons()
                            
                            wait(1000)
                            ev3.screen.draw_text(30,50, "Service Mode")

                            """
                            Send Notification to Node-Red Server
                            Machine currently in Service Mode
                            API to Content Delivery Network
                            """

                            if second_pressed:
                                brick.display.clear()
                                rfid.clearUID()
                                ev3.screen.load_image(ImageFile.EV3_ICON)
                                wait(2000)
                                break
                                
                                """
                                Send Notification to Node-Red Server
                                Machine in Standard Mode
                                """
                        break

            elif color == Color.BLUE:    
                brick.sound.file(SoundFile.BLUE)
                belt_motor.run_target(500, 5)
                eject()

            elif color == Color.GREEN:
                brick.sound.file(SoundFile.GREEN)
                belt_motor.run_target(500, 132)
                eject()

            elif color == Color.YELLOW:
                brick.sound.file(SoundFile.YELLOW)
                belt_motor.run_target(500, 357)
                eject()

            elif color == Color.RED:
                brick.sound.file(SoundFile.RED)
                belt_motor.run_target(500, 530)
                eject()
