class App:

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Keyboard"

    def run(self):
        self.badge.keyboard()
        return
