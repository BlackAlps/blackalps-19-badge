import network
import time
import machine
from ubinascii import hexlify
from umqtt.simple import MQTTClient
from .settings import *

class Net:

    def __init__(self):
        self.SSID = SSID
        self.KEY = KEY

        self.dev_name = b'badge-'+hexlify(machine.unique_id())

        self.sta = network.WLAN(network.STA_IF)


        self.client = MQTTClient(self.dev_name, 'mqtt.balda.ch', user='badge', password='badge')
        self.client.set_callback(self.mqtt_cb)
        self.CALLBACKS = {}

    def online(self):
        """
        Put badge online
        """
        self.sta.active(True)
        self.sta.connect(self.SSID, self.KEY)

        i=0
        while not self.sta.isconnected():
            time.sleep(1)
            i = i+1
            if i == 5:
                return False

        try:
            self.client.connect()
        except OSError:
            return False

        return True

    def offline(self):
        """
        Disconnect badge from network
        """
        try:
            self.client.disconnect()
        except OSError:
            pass
        self.sta.active(False)

    def add_callback(self, topic, cb):
        """
        Add MQTT callback

        topic is a topic name (bytes)
        cb is a function pointer. It need to have one parameter: the message
        """
        #TODO Add cb type checking
        self.CALLBACKS.update({topic:cb})
        self.client.subscribe(topic)

    def del_callback(self, topic):
        """
        Remove a MQTT callback
        """
        try:
            self.CALLBACKS.pop(topic)
        except KeyError:
            pass

    def mqtt_cb(self, topic, msg):
        """
        Base MQTt callback. Use add_callback() to add a new one
        """
        if topic in self.CALLBACKS.keys():
            self.CALLBACKS[topic](msg)
