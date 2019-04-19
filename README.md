# ev3-mqtt-micropython
Using LEGO MINDSTORMS EV3 MicroPyhton with MQTT

LEGO MicroPyhton release for MINDSTORMS EV3 includes 'umqtt.simple' and 'umqtt.robust' modules. This allows us to integrate our EV3 brick on a IoT environment through MQTT (over Wi-Fi). No need to dig into SSH or shell commands - just a Pyhton IDE that can connect to the EV3 is required, like the Visual Studio Code with the LEGO EV3 MicroPython extension.

We just need to import the required module, instantiate a MQTTClient and connect it to a MQTT broker:

```
from umqtt.robust import MQTTClient
client = MQTTClient(MQTT_ClientID, MQTT_Broker)
client.connect()
```
Where 'MQTT_ClientID' is a unique string that identifies our device from all others and 'MQTT_Broker' is the IP address or the hostname of an available MQTT Broker (like 'test.mosquitto.org' or our laptop if we installed a broker on it).

Then sending ('publishing)' messages through the broker is very simple:

```
client.publish(MQTT_Topic, Message)
```

where 'MQTT_Topic' is just a string that we chose to distinguish this message from any others (like a namespace).

To receive messages is a little less immediate as we need to subscribe to the topic(s) we want and also define a callback function that will process all messages received:

```
def getmessages(topic, msg):
    if topic == MQTT_Topic.encode():
        dosomethingwithmsg()
        
client.set_callback(getmessages)
client.subscribe(MQTT_Topic)
```

It's better to examine the included [main.py](https://github.com/JorgePe/ev3-mqtt-micropython/blob/master/main.py) script. It's meant to run on several EV3 bricks, using the hostname of each brick as the 'MQTT_ClientID' (assuming that default hostname wast changed after installation). The video bellow shows two bricks ('Iota' and 'Alpha') listening to the same topic and moving the motor axle to the position received on it.

[![EV3 MicroPython IoT](https://i9.ytimg.com/vi/UIqabk5VxZ0/mq1.jpg?sqp=CIiG2OUF&rs=AOn4CLD_D7mT6BSuXjQunY9w5N_CCmF_Cw)](https://youtu.be/UIqabk5VxZ0 "Micro:bit Ultrasonic Sensor and EV3")

Please note that this only works with a MQTT broker. There are public brokers available (like 'test.mosquitto.org') but we can run our own broker on our computer (just get the proper ['mosquitto'](https://mosquitto.org/) package for you system) or even on one of our EV3 (the ev3dev image inlcudes the whole mosquitto package, just start the broker service with 'sudo services mosquitto start'). There are also some Apps for mobile devices that can do the same.
