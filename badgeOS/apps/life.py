#!/usr/bin/env python3
import time
import random


class App:

    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Life"
        self.board = Board(badge, 16)

    def run(self):
        while self.badge.buttons.get_button() == None:
            self.badge.screen.textbox(["The game of life", "Keys spawn figures", "Enter quits", "Down clears"])

        self.board.clear()
        self.add_glider(5, 5)
        while True:
            self.board.print()
            key = self.badge.buttons.get_button()
            if key == "ENTER":
                return
            if key == "LEFT":
                self.add_glider()
            if key == "RIGHT":
                self.add_cross()
            if key == "UP":
                self.add_tub()
            if key == "DOWN":
                self.board.clear()
            self.evolve()

    def getRand(self, width, height):
        return random.randrange(self.board.sizex - width), random.randrange(self.board.sizey - height)

    def evolve(self):
        newBoard = Board(self.badge, self.board.sizey)
        for x in range(self.board.sizex):
            for y in range(self.board.sizey):
                neighbors = self.board.neighbors(x, y)
                if neighbors < 2:
                    newBoard.set(x, y, 0)
                if neighbors == 2:
                    newBoard.set(x, y, self.board.cells[x][y])
                if neighbors == 3:
                    newBoard.set(x, y, 1)
                if neighbors > 3:
                    newBoard.set(x, y, 0)
        self.board = newBoard

    def add_glider(self, x=-1, y=-1):
        if x < 0 and y < 0:
            x, y = self.getRand(3, 3)
        self.board.set(x + 1, y, 1)
        if random.randrange(2) == 0:
            self.board.set(x, y + 1, 1)
        else:
            self.board.set(x + 2, y + 1, 1)
        self.board.set(x, y + 2, 1)
        self.board.set(x + 1, y + 2, 1)
        self.board.set(x + 2, y + 2, 1)

    def add_cross(self, x=-1, y=-1):
        if x < 0 and y < 0:
            x, y = self.getRand(3, 3)
        self.board.set(x, y, 1)
        self.board.set(x, y + 1, 1)
        self.board.set(x, y + 2, 1)

    def add_tub(self, x=-1, y=-1):
        if x < 0 and y < 0:
            x, y = self.getRand(3, 3)
        self.board.set(x + 1, y, 1)
        self.board.set(x, y + 1, 1)
        self.board.set(x + 2, y + 1, 1)
        self.board.set(x + 1, y + 2, 1)


class Board:

    def __init__(self, badge, size):
        self.badge = badge
        self.sizex = size * 2
        self.sizey = size
        self.mul = int(64 / size)
        self.cells = [[0]]
        self.clear()

    def clear(self):
        self.cells = [[0] * self.sizey for i in range(self.sizex)]

    def print(self):
        self.badge.screen.oled.fill(0)
        self.badge.screen.oled.rect(0, 0, 128, 64, 1)
        for x in range(self.sizex):
            for y in range(self.sizey):
                if self.cells[x][y] > 0:
                    posx = x * self.mul
                    posy = y * self.mul
                    for i in range(self.mul):
                        self.badge.screen.oled.hline(posx, posy + i, self.mul, 1)
        self.badge.screen.oled.show()

    def set(self, x, y, v):
        if x < 0 or x >= self.sizex:
            print("oob", x, y)
            return
        if y < 0 or y >= self.sizey:
            print("oob", x, y)
            return
        self.cells[x][y] = v

    def neighbors(self, cx, cy):
        count = 0
        for x in range(cx - 1, cx + 2):
            for y in range(cy - 1, cy + 2):
                if x != cx or y != cy:
                    if self.cells[x % self.sizex][y % self.sizey] > 0:
                        count = count + 1
        return count


def test_nb():
    b = Board(0, 4)
    b.set(0, 0, 1)
    print(b.neighbors(0, 0))
    print(b.neighbors(1, 1))
    print(b.neighbors(7, 3))
    print(b.neighbors(7, 2))
    print(b.neighbors(7, 1))


if __name__ == "__main__":
    test_nb()
