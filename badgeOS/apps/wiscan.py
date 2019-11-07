class App:
    
    def __init__(self, badge):
        self.badge = badge
        self.oled = badge.screen.oled
        self.NAME = "WiFi Scanner"
        self.title = "> WiFi Scanner <"
        self.auth_mode = {0: "OPEN", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}

    def nice_display(self, entry):
        ssid_len = 12
        ssid = entry[0][:ssid_len].decode('ascii')
        ssid += " "*(ssid_len-len(ssid))
        s = "%s %02d" % (ssid, entry[2])
        return s

    def nice_display2(self, entry):
        ssid_len = 15
        ssid = entry[0][:ssid_len].decode('ascii')
        ssid += " "*(ssid_len-len(ssid))
        mac = "%02X%02X:%02X%02X:%02X%02X" % (entry[1][0],entry[1][1],entry[1][2],entry[1][3],entry[1][4],entry[1][5])
        channel = "CH%02d" % entry[2]
        power = "RSSI: %d" % entry[3]
        auth = "Auth: UNK"
        if entry[4] in self.auth_mode:
            auth = "Auth: %s" % self.auth_mode[entry[4]]
        return [ssid, mac, channel, power, auth]

    def testbtn(self):
        return self.badge.buttons.get_button() not in (None, 'ENTER')

    def runapp(self):
        if not self.badge.net.sta.active():
            self.badge.net.sta.active(True)
        self.badge.screen.clear()
        self.badge.set_title(self.title)
        self.badge.screen.textbox(("Scanning...",))
        scan_results = self.badge.net.sta.scan()
        l = []
        d = {}
        for e in scan_results:
            l.append(self.nice_display(e))
            d[self.nice_display(e)] = e
        while(True):
            self.badge.screen.clear()
            self.badge.set_title(self.title)
            choice = self.badge.menu(l)

            if choice not in d:
                break

            self.badge.screen.clear()
            self.badge.set_title(choice)
            self.badge.screen.textbox(self.nice_display2(d[choice]))
            while(True):
                if self.testbtn(): break
        return

    def run(self):
        self.runapp()