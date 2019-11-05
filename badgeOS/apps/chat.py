
class App:
    """
    Chat app

    This app uses the MQTT publish/subscribe mechanism to show a live "chat"
    Messages can be sent within the app, and the messges are shown live on the screen
    """

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Moo-ter"

        self.moots = []

    def moot_cb(self, moot):
        """
        MQTT callback for new moots
        """
        self.moots.append(moot.decode())
        if len(self.moots) > 5:
            self.moots = self.moots[-5:]

    def run(self):
        if self.badge.net.online():
            self.badge.net.add_callback(b'BA19/mooter/moots', self.moot_cb)
            self.badge.set_title("Mootter")

            while(1):
                self.badge.net.client.check_msg()
                self.badge.screen.textbox(self.moots)
                btn = self.badge.buttons.get_button()
                if btn == 'ENTER':
                    msg = self.badge.prompt("Send a Moot")
                    self.badge.net.client.publish(b'BA19/mooter/moots', msg)
                    continue
                elif btn is not None:
                    print(self.badge.buttons.get_button())
                    break
        self.badge.net.del_callback(b'BA19/mooter/moots')
        self.badge.net.offline()
        return

