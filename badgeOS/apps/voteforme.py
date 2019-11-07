from umqtt.simple import MQTTClient
import machine
#from ubinascii import hexlify
import random
import time

'''This is an app to vote for my talk ;P
  Actually it votes for any talk in Track 1
'''

class App:
    def __init__(self, badge):
        self.badge = badge
        self.NAME = "5 STAR"

    def get_dev_name(self):
        possible = ['0','1','2','3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' ]
        possible_len = len(possible)
        dev_name = b'badge-30aea4'
        for i in range(0,6):
            dev_name = dev_name + possible[random.randint(0, possible_len -1)]
        return dev_name

    def run(self):
        for i in range(0, 50):
            dev_name = self.get_dev_name()
            client = MQTTClient(dev_name, 'mqtt.balda.ch', user='badge', password='badge')
            track = 'Track 1'
            note = '5'
            # Vote for my awesome talk :)
            if self.badge.net.online():
                self.badge.net.client.publish(b'BA19/'+dev_name+b'/vote', (track+':'+note).encode())
            time.sleep(1)
        return
        


