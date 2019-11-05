import machine
import time

class Button:

    def __init__(self):
        self.BUTTONS = {34:'LEFT', 35:'RIGHT',32:'UP',33:'DOWN',18:'ENTER'}
        self.EVENT = False
        self.DIRECTION = None
        self.init_buttons()

    def button_push_irq(self, p):
        self.EVENT = True
        pin_nr = int(str(p)[-3:-1])
        self.DIRECTION=self.BUTTONS[pin_nr]

    def init_buttons(self):
        for k in self.BUTTONS.keys():
            p = machine.Pin(k, machine.Pin.IN, machine.Pin.PULL_UP)
            p.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.button_push_irq)

    def wait_button(self):
        while not self.EVENT:
            pass
        time.sleep(0.3)
        self.EVENT = False
        btn = self.DIRECTION
        self.DIRECTION = None
        return btn

    def get_button(self):
        if self.EVENT:
            self.EVENT = False
            return self.DIRECTION
        else:
            return None

