import sys
import importlib
import pygame
import time
import os
from pygame.locals import *


class Buttons:

    def get_button(self):
        time.sleep(0.1)
        for event in pygame.event.get():
            if (event.type == KEYDOWN):
                if event.key == K_RETURN:
                    return "ENTER"
                if event.key == K_LEFT:
                    return "LEFT"
                if event.key == K_RIGHT:
                    return "RIGHT"
                if event.key == K_DOWN:
                    return "DOWN"
                if event.key == K_UP:
                    return "UP"
                if event.key == K_q:
                    os._exit(1)


class Oled:
    def __init__(self):
        self.x = 128
        self.y = 64
        # Will be initialized so it can be used as pixels[x][y]
        self.pixels = [[0]]
        self.fill(0)

    def pixel(self, x, y, v):
        self.pixels[x][y] = v

    def fill(self, v):
        self.pixels = [[v] * self.y for i in range(self.x)]

    def rect(self, x, y, x2, y2, v):
        self.hline(x, y, x2 - x, v)
        self.vline(x2, y, y2 - y, v)
        self.hline(x+1, y2, x2 - x, v)
        self.vline(x, y+1, y2 - y, v)

    def vline(self, x, y, height, v):
        if x < 0 or x >= self.x:
            return
        if y < 0 or y >= self.y:
            return
        for i in range(int(min(height, self.y - y))):
            self.pixels[int(x)][int(y+i)] = v

    def hline(self, x, y, width, v):
        if x < 0 or x >= self.x:
            return
        if y < 0 or y >= self.y:
            return
        for i in range(int(min(width, self.x - x))):
            self.pixels[int(x+i)][int(y)] = v

    def show(self):
        print("\033[;H", end='')
        for y in range(self.y):
            for x in range(self.x):
                print("**" if self.pixels[x][y] > 0 else "  ", end='')
            print()


class Screen:

    def __init__(self):
        self.oled = Oled()


class Badge:

    def __init__(self):
        self.screen = Screen()
        self.buttons = Buttons()


if __name__ == "__main__":
    userApp = importlib.import_module(".", sys.argv[1].replace(".py", ""))
    pygame.init()
    a = userApp.App(Badge())

    a.run()
