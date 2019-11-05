#!/usr/bin/env python3

"""Picross game implementation for the Black Alps 19 badge.

Sorry for any code duplication. Had to finish this in a hurry.

- Nils"""

import uos

import font454

# screen
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# text
FONT_SIZE = 8

# grid
GRID_SIZE_X = 10
GRID_SIZE_Y = 5
GRID_START_X = 40
GRID_START_Y = 24

GRID_SPACING = FONT_SIZE
GRID_WIDTH = GRID_SIZE_X * GRID_SPACING
GRID_HEIGHT = GRID_SIZE_Y * GRID_SPACING

# hints
HINTS_SIZE_X = 5
HINTS_SIZE_Y = 3

# cells
EMPTY = 0
FILLED = 1
CROSSED = 2


class App:
    def __init__(self, badge):
        self.badge = badge
        self.NAME = "Picross"

        self.CURSOR_X = 0
        self.CURSOR_Y = 0
        self.GRID = []
        self.SOLUTION_GRID = []
        self.HINTS_ROWS = []
        self.HINTS_COLUMNS = []

        self.reset_game_state()

    def reset_game_state(self):
        """Reset the game state."""
        # game state
        self.CURSOR_X = 0
        self.CURSOR_Y = 0
        self.GRID = []
        self.SOLUTION_GRID = []
        self.HINTS_ROWS = []
        self.HINTS_COLUMNS = []
        for i in range(GRID_SIZE_X):
            self.GRID.append([])
            self.SOLUTION_GRID.append([])

        for i in range(GRID_SIZE_X):
            for j in range(GRID_SIZE_Y):
                self.GRID[i].append(EMPTY)
                self.SOLUTION_GRID[i].append(EMPTY)

        for i in range(GRID_SIZE_X):
            self.HINTS_COLUMNS.append([])
        for i in range(GRID_SIZE_Y):
            self.HINTS_ROWS.append([])

    def generate_puzzle(self):
        """Generate a random solution and derive the hints based on that generated solution."""
        # generate random solution grid
        for i in range(GRID_SIZE_X):
            for j in range(GRID_SIZE_Y):
                random = ord(uos.urandom(1)) % 2
                self.SOLUTION_GRID[i][j] = random

        # column hints
        for x in range(GRID_SIZE_X):
            self.HINTS_COLUMNS[x] = []
            group_size = 0
            for y in range(GRID_SIZE_Y):
                cell = self.SOLUTION_GRID[x][y]
                if cell == FILLED:
                    group_size += 1
                elif cell == EMPTY and group_size > 0:
                    self.HINTS_COLUMNS[x].append(group_size)
                    group_size = 0
            # all rows processed
            if len(self.HINTS_COLUMNS[x]) == 0 or group_size > 0:
                self.HINTS_COLUMNS[x].append(group_size)

        # row hints
        for y in range(GRID_SIZE_Y):
            self.HINTS_ROWS[y] = []
            group_size = 0
            for x in range(GRID_SIZE_X):
                cell = self.SOLUTION_GRID[x][y]
                if cell == FILLED:
                    group_size += 1
                elif cell == EMPTY and group_size > 0:
                    self.HINTS_ROWS[y].append(group_size)
                    group_size = 0
            # all columns processed
            if len(self.HINTS_ROWS[y]) == 0 or group_size > 0:
                self.HINTS_ROWS[y].append(group_size)

    def tiny(self, text, x, y):
        """Display the given `text`at position (`x`, `y`) with a tiny font."""
        font454.text(self.badge.screen.oled, text, x0=x, y0=y)

    def reset_screen(self):
        """Reset the screen."""
        self.badge.screen.oled.fill(0)

    def draw_filled_cell(self, x, y):
        """Draw a filled cell."""
        for px in range(x, x + GRID_SPACING - 1):
            for py in range(y, y + GRID_SPACING - 1):
                self.badge.screen.oled.pixel(px, py, 1)

    def draw_cursor_cell(self, x, y):
        """Draw the cursor cell."""
        cell_state = self.GRID[self.CURSOR_X][self.CURSOR_Y]
        color = 1
        if cell_state == FILLED:
            color = 0
        self.badge.screen.oled.rect(x + 1, y + 1, GRID_SPACING - 1, GRID_SPACING - 1, color)

    def draw_crossed_cell(self, x, y):
        """Draw a crossed cell."""
        for px in range(x, x + GRID_SPACING - 1):
            dx = px - x
            for py in range(y, y + GRID_SPACING - 1):
                dy = py - y
                if dx == dy or dx + dy == GRID_SPACING - 2:
                    self.badge.screen.oled.pixel(px, py, 1)

    def draw_grid(self):
        """Draw the grid lines."""
        # draw vertical lines
        for px in range(GRID_START_X, SCREEN_WIDTH, GRID_SPACING):
            self.badge.screen.oled.vline(px, GRID_START_Y, GRID_HEIGHT, 1)

        # draw horizontal lines
        for py in range(GRID_START_Y, SCREEN_HEIGHT, GRID_SPACING):
            self.badge.screen.oled.hline(GRID_START_X, py, GRID_WIDTH, 1)

    def draw_blackalps_logo(self):
        """Draw a Black Alps logo in the top left corner."""
        self.tiny("Blk Alps", 0, 0)
        self.tiny("2k19", 0, 7)

    def is_completed(self):
        """
        Returns true if the current grid is a valid solution.

        Build hints for the current grid and check that they match the generated solution hints.
        This is required because sometimes puzzles can have multiple solutions and
        simply checking whether GRID == SOLUTION_GRID won't work if the player
        solved the puzzle with another solution than the one that was generated.
        """
        #
        expected_hints_columns = []
        expected_hints_rows = []

        for i in range(GRID_SIZE_X):
            expected_hints_columns.append([])
        for i in range(GRID_SIZE_Y):
            expected_hints_rows.append([])

        for x in range(GRID_SIZE_X):
            expected_hints_columns[x] = []
            group_size = 0
            for y in range(GRID_SIZE_Y):
                cell = self.GRID[x][y]
                if cell == FILLED:
                    group_size += 1
                elif cell != FILLED and group_size > 0:
                    expected_hints_columns[x].append(group_size)
                    group_size = 0
            # all rows processed
            if len(expected_hints_columns[x]) == 0 or group_size > 0:
                expected_hints_columns[x].append(group_size)

        # row hints
        for y in range(GRID_SIZE_Y):
            expected_hints_rows[y] = []
            group_size = 0
            for x in range(GRID_SIZE_X):
                cell = self.GRID[x][y]
                if cell == FILLED:
                    group_size += 1
                elif cell != FILLED and group_size > 0:
                    expected_hints_rows[y].append(group_size)
                    group_size = 0
            # all columns processed
            if len(expected_hints_rows[y]) == 0 or group_size > 0:
                expected_hints_rows[y].append(group_size)

        # check that hints match
        return expected_hints_rows == self.HINTS_ROWS and expected_hints_columns == self.HINTS_COLUMNS

    def draw(self):
        """Draw the game on screen."""
        self.reset_screen()

        if self.is_completed():
            self.tiny("COMPLETED!", 0, 0)
        else:
            self.draw_blackalps_logo()
        self.draw_hints()
        self.draw_grid()
        self.draw_cell_filling()
        self.draw_cursor()

        # refresh the screen
        self.badge.screen.oled.show()

    def draw_cell_filling(self):
        """Draw each cell in the grid."""
        for i in range(GRID_SIZE_X):
            for j in range(GRID_SIZE_Y):
                cell_x = GRID_START_X + i * GRID_SPACING + 1
                cell_y = GRID_START_Y + j * GRID_SPACING + 1
                cell_state = self.GRID[i][j]

                if cell_state == FILLED:
                    self.draw_filled_cell(cell_x, cell_y)
                elif cell_state == CROSSED:
                    self.draw_crossed_cell(cell_x, cell_y)

    def draw_hints(self):
        """Draw row and column hints."""
        # draw column hints
        for col in range(GRID_SIZE_X):
            hints = self.HINTS_COLUMNS[col]
            x = GRID_START_X + GRID_SPACING * col
            y = GRID_START_Y - FONT_SIZE

            for hint in hints[::-1]:
                self.badge.screen.oled.text(str(hint), x, y)
                y = y - FONT_SIZE

        # draw row hints
        for row in range(GRID_SIZE_Y):
            hints = self.HINTS_ROWS[row]
            x = GRID_START_X - FONT_SIZE
            y = GRID_START_Y + GRID_SPACING * row

            for hint in hints[::-1]:
                self.badge.screen.oled.text(str(hint), x, y)
                x = x - FONT_SIZE

    def draw_cursor(self):
        """Draw the cursor at the appropriate location."""
        cell_x = GRID_START_X + self.CURSOR_X * GRID_SPACING
        cell_y = GRID_START_Y + self.CURSOR_Y * GRID_SPACING
        self.draw_cursor_cell(cell_x, cell_y)

    def toggle_cell(self):
        """Toggle the state of the selected cell."""
        self.GRID[self.CURSOR_X][self.CURSOR_Y] = (self.GRID[self.CURSOR_X][self.CURSOR_Y] + 1) % 3

    def run(self):
        """Start the game."""
        self.reset_game_state()
        self.generate_puzzle()
        self.draw()
        cpt = 0

        completed = False

        while True:
            key = self.badge.buttons.wait_button()

            if completed:
                return

            if key == 'LEFT':
                self.CURSOR_X = (self.CURSOR_X - 1) % GRID_SIZE_X
                cpt = 0
            elif key == 'RIGHT':
                self.CURSOR_X = (self.CURSOR_X + 1) % GRID_SIZE_X
                cpt = 0
            elif key == 'UP':
                self.CURSOR_Y = (self.CURSOR_Y - 1) % GRID_SIZE_Y
                cpt = 0
            elif key == 'DOWN':
                self.CURSOR_Y = (self.CURSOR_Y + 1) % GRID_SIZE_Y
                cpt = 0
            elif key == 'ENTER':
                cpt = cpt+1
                if cpt>4:
                    self.badge.set_title("Quit ?")
                    rsp = self.badge.menu(['Yes','No'])
                    if rsp == 'Yes':
                        return
                    else:
                        cpt = 0
                if not completed:
                    self.toggle_cell()

                if self.is_completed():
                    completed = True

            else:
                pass
            self.draw()
