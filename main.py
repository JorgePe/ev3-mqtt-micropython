#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

from umqtt.robust import MQTTClient
import time
import os

motor = Motor(Port.A)

########################################################################
# get hostname to use as Client ID
# assuming each EV3 brick had it's hostname changed after installation
########################################################################
os.system('hostname > /dev/shm/hostname.txt')
file = open('/dev/shm/hostname.txt', 'r')
MQTT_ClientID = file.readline().rstrip('\n')
file.close()
os.system('rm /dev/shm/hostname.txt')

########################################################################
# There are public brokers available but you we can also install
# 'mosquitto' and run our own private broker
# note: ev3dev image already has 'mosquitto' instaled, we can start the
# broker with 'sudo service mosquitto start'
########################################################################
#MQTT_Broker = 'test.mosquitto.org'
MQTT_Broker = '10.24.10.121'

# Define a namespace for all messages
MQTT_Topic_Status = 'JorgePe/Status'
MQTT_Topic_Motor = 'JorgePe/Motor'

# callback message to process any new message appearing at the subscribed
# topics
def getmessages(topic, msg):
    if topic == MQTT_Topic_Status.encode():
        brick.display.text(str(msg.decode()))
    elif topic == MQTT_Topic_Motor.encode():
        brick.display.text(str(msg.decode()))
        motor.run_target(180, int(msg.decode()))


motor.reset_angle(0)

client = MQTTClient(MQTT_ClientID, MQTT_Broker)
client.connect()

client.publish(MQTT_Topic_Status, MQTT_ClientID + ' Started')
client.set_callback(getmessages)
client.subscribe(MQTT_Topic_Status)
client.subscribe(MQTT_Topic_Motor)
client.publish(MQTT_Topic_Status, MQTT_ClientID + ' Listening')

while True:
    client.check_msg()
    time.sleep(0.1)
