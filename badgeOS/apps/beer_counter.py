__author__  = "Gerhard K. (@iiiikarus)"
__copyright__ = "Copyright 2019"
__license__ = "GPLv3"
__version__ = "1.0.0"


class App:

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Beer Counter"
        self.beers = 0
        self.drunk_level = 0
        self.drunk_stats = ["A little bit shy",
                            "Everything is fine",
                            "Talking to random people",
                            "Talking too much to random people",
                            "It's hard to understand you",
                            "You need subtitles",
                            "Talking to objects instead of people",
                            "Can't walk anymore",
                            "Checking what the floor smells like",
                            "Over 9000"]


    def run(self):
        # Init screen.
        self.badge.screen.clear()
        self.badge.set_title("Beer Counter")
        # Restore counter.
        self.restore_counter()

        # Main loop.
        while True:
            # Set the drunk level.
            if (self.beers >= len(self.drunk_stats * 2)):
                self.drunk_level = len(self.drunk_stats) - 1
            else:
                self.drunk_level = int(self.beers/2)

            # Display the results.
            text = ["Beers: {}".format(self.beers), "Level:"]
            text = text + \
                self.word_wrap(self.drunk_stats[self.drunk_level], 16)
            self.badge.screen.textbox(text)

            # Check for keys.
            key = self.badge.buttons.get_button()
            if key == None:
                continue
            if key == 'UP':
                self.beers += 1
            elif key == 'DOWN':
                if self.beers > 0:
                    self.beers -= 1
            else:
                # Save counter & exit app.
                self.save_counter()
                break


    def restore_counter(self):
        try:
            with open('beer_counter_settings.txt', 'r') as f:
                self.beers = int(f.read())
                f.close()
        except:
            pass


    def save_counter(self):
        try:
            with open('beer_counter_settings.txt', 'w') as f:
                f.write(str(self.beers))
                f.close()
        except:
            pass


    # Need word wrapping, but badge.show_text() has scrolling...
    @staticmethod
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
