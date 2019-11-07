import time
import machine
import math
import urequests

class App:

    CX = 64 # Center X position
    CY = 32 # Center Y position

    H = 20 # Hour hand length
    M = 28 # Minute hand length
    S = 15 # Second hand length

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Clock"
        self.rtc = machine.RTC()

    def draw_face(self):
        p = 360/12 # Portion divider

        self.badge.screen.oled.fill(0)

        for i in range(12):
            x = self.CX+int(30*math.cos(math.radians(p*i)))
            y = self.CY+int(30*math.sin(math.radians(p*i)))
            self.badge.screen.oled.pixel(x,y,1)

    def draw_hours(self):
        p = 360/12 # Portion divider

        hour = 3-(self.rtc.datetime()[4] % 12)
        hour = -hour

        x = self.CX+int(self.H*math.cos(math.radians(p*hour)))
        y = self.CY+int(self.H*math.sin(math.radians(p*hour)))
        self.badge.screen.oled.line(self.CX, self.CY, x, y, 1)

    def draw_minutes(self):
        p = 360/60 # Portion divider
        minute = 15-(self.rtc.datetime()[5])
        minute = -minute

        x = self.CX+int(self.M*math.cos(math.radians(p*minute)))
        y = self.CY+int(self.M*math.sin(math.radians(p*minute)))
        self.badge.screen.oled.line(self.CX, self.CY, x, y, 1)


    def draw_seconds(self):
        p = 360/60 # Portion divider
        second = 15-(self.rtc.datetime()[6])
        second = -second

        x = self.CX+int(self.S*math.cos(math.radians(p*second)))
        y = self.CY+int(self.S*math.sin(math.radians(p*second)))
        self.badge.screen.oled.line(self.CX, self.CY, x, y, 1)

    def run(self):
        #self.badge.net.online()
        #resp = urequests.get('http://worldtimeapi.org/api/timezone/Europe/Zurich')
        #dt = resp.json()
        #self.rtc.init(time.localtime(dt['unixtime']-946684800))
        #self.badge.net.offline()

        while(True):
            self.draw_face()
            self.draw_hours()
            self.draw_minutes()
            self.draw_seconds()
            self.badge.screen.oled.show()
            time.sleep(1)
            if self.badge.buttons.get_button() == 'ENTER':
                return
        return


