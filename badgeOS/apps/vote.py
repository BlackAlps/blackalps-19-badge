class App:
    """
    Simple voting app.

    This app shows how to publish something on the MQTT server
    Data will be collected by the organizers along the conference
    """

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Vote"

    def run(self):
        self.badge.screen.oled.fill(0)
        self.badge.set_title("Which track ?")
        track = self.badge.menu(['Track 1', 'Track 2'])
        self.badge.screen.oled.fill(0)
        self.badge.set_title("How many stars ?")
        note = self.badge.menu(['5', '4', '3', '2', '1'])
        if self.badge.net.online():
            self.badge.net.client.publish(b'BA19/'+self.badge.net.dev_name+b'/vote', (track+':'+note).encode())
            self.badge.net.offline()
        else:
            self.badge.show_text("Error sending vote. Please try again.")
        return

