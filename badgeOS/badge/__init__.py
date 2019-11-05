from .button import Button
from .screen import Screen
from .net import Net

class Badge:

    def __init__(self):
        self.buttons = Button()
        self.screen = Screen()
        self.net = Net()

    def menu(self, items):
        """
        Draws a menu and handles the UI

        items is a list of menu entries

        Returns the selected menu entry
        """
        MENU_LEN = 5
        pages = [items[i:i+MENU_LEN] for i in range(0, len(items), MENU_LEN)]
        page = 0
        pos = 0
        self.screen.oled.fill_rect(0,12,128,52,0)
        self.screen.oled.rect(0,12,128,52,1)
        while 1:
            self.screen.draw_menu(pages[page], pos)
            btn = self.buttons.wait_button()
            if btn == 'UP':
                if pos == 0:
                    page = (page -1) % len(pages)
                    pos = len(pages[page])-1
                    self.screen.oled.fill_rect(0,12,128,52,0)
                    self.screen.oled.rect(0,12,128,52,1)
                else:
                    pos = pos -1
            elif btn == 'DOWN':
                if pos == len(pages[page])-1:
                    page = (page + 1) % len(pages)
                    pos = 0
                    self.screen.oled.fill_rect(0,12,128,52,0)
                    self.screen.oled.rect(0,12,128,52,1)
                else:
                    pos = pos + 1
            elif btn == 'LEFT':
                return None
            elif btn == 'ENTER':
                return pages[page][pos]

    def show_text(self, text):
        """
        Shows text to the user.
        The text is automatically word wrapped and can be scrolled by the user

        """
        # https://www.saltycrane.com/blog/2007/09/python-word-wrap-function/
        def word_wrap(string, width=80, ind1=0, ind2=0, prefix=''):
            string = prefix + ind1 * " " + string
            newstring = ""
            while len(string) > width:
                marker = width - 1
                while not string[marker].isspace():
                    marker = marker - 1

                newline = string[0:marker] + "\n"
                newstring = newstring + newline
                string = prefix + ind2 * " " + string[marker + 1:]

            return (newstring + string).split('\n')

        pos = 0
        lines  = word_wrap(text, 16)
        while 1:
            self.screen.textbox(lines[pos:pos+5])
            btn = self.buttons.wait_button()
            if btn == 'UP':
                pos = pos - 1
            elif btn == 'DOWN':
                pos = pos + 1
            elif btn == 'LEFT':
                pos = pos - 5
            elif btn == 'RIGHT':
                pos = pos + 5
            elif btn == 'ENTER':
                return
            pos = pos % len(lines)

    def prompt(self, prompt):
        """
        Prompt for a user input.

        Returns the input string
        """
        CHARSET = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        index = 0
        val = list(' '*15)

        while 1:
            self.screen.oled.fill_rect(0,12,128,52,0)
            self.screen.oled.rect(0,12,128,52,1)

            self.screen.textbox([prompt], 0)
            self.screen.oled.text("_", 2+(10*index), 30)
            for i in range(15):
                self.screen.oled.text(val[i], 2+(10*i), 28)
            self.screen.oled.show()

            btn = self.buttons.wait_button()
            if btn == 'LEFT':
                index = (index-1)%15
            elif btn == 'RIGHT':
                index = (index+1)%15
            elif btn == 'UP':
                val[index] = CHARSET[(CHARSET.index(val[index]) + 1) % len(CHARSET)]
            elif btn == 'DOWN':
                val[index] = CHARSET[(CHARSET.index(val[index]) - 1) % len(CHARSET)]
            elif btn == 'ENTER':
                return ''.join(val)

    def set_title(self, title):
        """
        Set screen title
        """
        self.screen.oled.fill_rect(0,0,128,11,0)
        self.screen.text(title, 0, 0)
