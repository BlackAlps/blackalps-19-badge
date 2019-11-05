import machine
import sys
import os
import time

import badge

machine.freq(80000000)

BADGE = badge.Badge()
BADGE.screen.show_logo()

APPS = {}
SCHEDULE = ''

def app_load():
    global APPS
    modules = os.listdir('apps')
    for module in modules:
        try:
            m = __import__('apps.'+module[:-3], globals(), locals(), ['App'])
            app = m.App(BADGE)
            APPS.update({app.NAME: app})
        except Exception as e:
            sys.print_exception(e)
            continue

# Load apps
app_load()

try:
    while 1:
        #Main menu
        BADGE.screen.clear()
        BADGE.set_title("BadgeOS 0.2")
        choice = BADGE.menu(list(APPS.keys()) + ['test'])

        #Test submenu
        if choice == 'test':
            test_choice = BADGE.menu(['text', 'logo', 'prompt'])
            if test_choice == 'text':
                BADGE.show_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            elif test_choice == 'logo':
                BADGE.screen.show_logo()
                BADGE.buttons.wait_button()
            elif test_choice == 'prompt':
                BADGE.show_text(BADGE.prompt('Insert text'))

        #Run apps
        elif choice in APPS.keys():
            APPS[choice].run()
        else:
            pass
except Exception as e:
    sys.print_exception(e)
    machine.reset()
