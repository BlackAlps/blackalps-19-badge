import urequests

class App:

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Schedule"

    def run(self):
        if self.badge.net.online():
            response = urequests.get('https://blackalps.ch/ba-19/badges/next.php')
            try:
                data = response.json()
            except ValueError:
                self.badge.show_text("Invalid JSON received")
                self.badge.net.offline()
                return

            self.badge.net.offline()
            self.badge.set_title("What's next")

            text = list(data.keys())[0]
            text += '\n'
            for talk in list(data.values())[0]:
                text += talk
                text += '\n'

            self.badge.show_text(text)

