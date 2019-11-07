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

    def symbole_del(self, x, y, invert=False):
        self.screen.oled.fill_rect(x-1, y-1, 20, 10, invert)
        self.screen.oled.line(x, y + 4,     x + 8, y, not invert)
        self.screen.oled.line(x, y + 4,     x + 8, y + 8, not invert)
        self.screen.oled.line(x + 8, y,     x + 18, y, not invert)
        self.screen.oled.line(x + 8, y + 8, x + 18, y + 8, not invert)
        self.screen.oled.line(x + 18, y, x + 18, y + 8, not invert)

    def symbole_enter(self, x, y, invert=False):
        self.screen.oled.fill_rect(x-1, y-1, 10, 10, invert)
        self.screen.oled.line(x + 8, y, x + 8, y + 4, not invert)
        self.screen.oled.line(x, y + 4, x + 8, y + 4, not invert)
        self.screen.oled.line(x, y + 4, x + 4, y + 1, not invert)
        self.screen.oled.line(x, y + 4, x + 4, y + 7, not invert)

    def keyboard(self):
        LOWER = ['qwertyuiop\b',
                 'asdfghjkl\n',
                 'zxcv   bnm.\a']
        UPPER = ['QWERTYUIOP\b',
                 'ASDFGHJKL\n',
                 'ZXCV   BNM!\a']
        kb = UPPER
        row = 0
        col = 0
        val = list(' '*15)
        idx = 0
        capslock = kb == UPPER
        redraw = True
        self.screen.oled.fill_rect(0,12,128,52,0)
        self.screen.oled.rect(0,12,128,52,1)
        while True:
            col = min(col, len(kb[row]) - 1)
            if redraw:
                redraw = False
                self.screen.oled.fill_rect(1, 30, 126, 30, 0) # erease old keyboard
                self.symbole_del(104, 34, False)
                self.symbole_enter(94, 44, False)
                self.screen.oled.rect(5 + 10 * 4, 33 + 10 * 2, 28, 8, True)
                for r in [0, 1, 2]:
                    for i in range(len(kb[r])):
                        if not kb[r][i] in ('\b', '\n') :
                            self.screen.oled.text(kb[r][i], 4 + 10 * i, 34 + 10 * r)
            if kb[row][col] == '\b':
                self.symbole_del(104, 34, True)
            elif kb[row][col] == '\n':
                self.symbole_enter(94, 44, True)
            elif row == 2 and col > 3 and col < 7:
                self.screen.oled.fill_rect(4 + 10 * 4, 32 + 10 * 2, 30, 10, True)
                self.screen.oled.rect(5 + 10 * 4, 33 + 10 * 2, 28, 8, False)
            else:
                self.screen.oled.fill_rect(4 + 10 * col, 32 + 10 * row, 10, 10, True)
                self.screen.oled.text(kb[row][col], 4 + 10 * col, 34 + 10 * row, False)
            self.screen.oled.show()
            btn = self.buttons.wait_button()
            if kb[row][col] == '\b':
                self.symbole_del(104, 34, False)
            elif kb[row][col] == '\n':
                self.symbole_enter(94, 44, False)
            elif row == 2 and col > 3 and col < 7:
                self.screen.oled.fill_rect(4 + 10 * 4, 32 + 10 * 2, 30, 10, False)
                self.screen.oled.rect(5 + 10 * 4, 33 + 10 * 2, 28, 8, True)
            else:
                self.screen.oled.fill_rect(4 + 10 * col, 32 + 10 * row, 10, 10, False)
                self.screen.oled.text(kb[row][col], 4 + 10 * col, 34 + 10 * row, True)
            if row == 2 and col > 3 and col < 7:
                if btn == 'UP':
                    row = 1
                    col = 5
                elif btn == 'DOWN':
                    row = 0
                    col = 5
                elif btn == 'LEFT':
                    col = 3
                elif btn == 'RIGHT':
                    col = 7
                elif btn == 'ENTER':
                    val[idx] = ' '
                    self.screen.oled.fill_rect(2 + 8 * idx, 20, 8, 10, False)
                    self.screen.oled.text(val[idx], 2 + 8 * idx, 20)
                    idx = (idx + 1) % 15;
            else:
                if btn == 'UP':
                    row = (row - 1) % 3
                elif btn == 'DOWN':
                    row = (row + 1) % 3
                elif btn == 'LEFT':
                    col = (col - 1) % len(kb[row])
                elif btn == 'RIGHT':
                    col = (col + 1) % len(kb[row])
                elif btn == 'ENTER':
                    if kb[row][col] == '\a':
                        redraw = True
                        capslock = not capslock
                        if capslock:
                            kb = UPPER
                        else:
                            kb = LOWER
                    elif kb[row][col] == '\n':
                        return ''.join(val)
                    elif kb[row][col] == '\b':
                        idx = max(idx - 1, 0)
                        val[idx] = ' '
                        self.screen.oled.fill_rect(2 + 8 * idx, 20, 8, 10, False)
                    else:
                        val[idx] = kb[row][col]
                        self.screen.oled.fill_rect(2 + 8 * idx, 20, 8, 10, False)
                        self.screen.oled.text(val[idx], 2 + 8 * idx, 20)
                        idx = (idx + 1) % 15;

    def set_title(self, title):
        """
        Set screen title
        """
        self.screen.oled.fill_rect(0,0,128,11,0)
        self.screen.text(title, 0, 0)
