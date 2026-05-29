from PIL import ImageGrab
from time import sleep
import numpy as np
import pyautogui

class Puzzle:
    def __init__(self, size):
        self.size = size

        # The colors are IDs corresponding to colors stored in the color map.
        self.colors = np.zeros((size, size), dtype=int)
        self.color_map = {}   # color (r, g, b) -> ID (int)

        # 0: Open, 1: Marked, 2: Queen
        self.marks = np.zeros((size, size), dtype=int)

    def mark(self, loc, mark):

        # If the mark is outside of bounds, disregard it.
        if not 0 <= loc[0] < self.size or not 0 <= loc[1] < self.size:
            return

        if mark == 0 or mark == 1:
            self.marks[loc] = mark
        elif mark == 2:
            pass

            # 1. Lines
            self.marks[loc[1]] = 1
            self.marks[:, loc[0]] = 1

            # 2. Corners
            dx = (
                max(loc[1] - 1, 0),
                min(loc[1] + 1, self.size - 1)
            )
            dy = (
                max(loc[0] - 1, 0),
                min(loc[0] + 1, self.size - 1)
            )
            self.marks[dx[0], dy[0]] = 1
            self.marks[dx[0], dy[1]] = 1
            self.marks[dx[1], dy[0]] = 1
            self.marks[dx[1], dy[1]] = 1

            # 3. Queen
            self.marks[loc[1], loc[0]] = 2
        else:
            raise ValueError(f"Invalid mark: {mark}")

    # Determines if the puzzle has the correct amount of queens
    def is_solved(self):
        unique, counts = np.unique(self.marks, return_counts=True)
        return dict(zip(unique, counts))[2] == self.size

    # Determines if the solution is valid
    # Only needs to validate colors because the queens automatically mark each other if in the same row/col
    def is_valid(self):

        # Ensure the puzzle is solved
        if self.is_solved():

            # Create a dictionary of colors and queens
            keys = [n for n in range(self.size)]
            queens = dict.fromkeys(keys, 0)

            # Iterate through each cell
            for row in range(self.size):
                for col in range(self.size):
                    if self.marks[row, col] == 2:
                        queens[int(self.colors[row, col])] += 1

            # Check if each color has the same value
            return len(set(queens.values())) == 1 and queens[0] == 1
        return False

    # Scans screen to populate self.colors
    def build(self, start, end):

        # First, alt-tab to the correct screen
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        pyautogui.keyUp("alt")

        # Next, start the game.
        start_x = start[0] + 0.5 * (end[0] - start[0])
        start_y = start[1] + 0.5 * (end[1] - start[1])
        pyautogui.leftClick(start_x, start_y)

        # Get mouse off-screen and wait a sec
        pyautogui.moveTo(max(0, start[0] - 100), max(0, start[1] - 100))
        sleep(0.25)

        # Figure out cell length and height
        cell_length = (end[0] - start[0]) / self.size
        cell_height = (end[1] - start[1]) / self.size

        # Gets color of each cell
        screen = ImageGrab.grab()
        for row in range(self.size):
            for col in range(self.size):
                pos_x = start[0] + (col + 0.5) * cell_length
                pos_y = start[1] + (row + 0.5) * cell_height

                color = screen.getpixel((pos_x, pos_y))

                # If there is an entry for this color in self.color_map, apply it
                if color in self.color_map.keys():
                    self.colors[row, col] = self.color_map[color]

                # If there isn't, make a new entry and apply it.
                else:
                    # Get the new ID
                    new_id = len(self.color_map)
                    self.color_map[color] = new_id

                    self.colors[row, col] = new_id

    # Resets puzzle
    def reset(self):
        self.__init__(self.size)

    # Applies the desired marks to the grid
    def apply(self, start, end, mark=2):
        cell_length = (end[0] - start[0]) / self.size
        cell_height = (end[1] - start[1]) / self.size

        # Iterate over each row and column and find the positions
        for row in range(self.size):
            for col in range(self.size):
                pos_x = start[0] + (col + 0.5) * cell_length
                pos_y = start[1] + (row + 0.5) * cell_height

                # Figure out whether to mark and do so
                if self.marks[row, col] == 2 and mark == 2:
                    pyautogui.leftClick(pos_x, pos_y)
                    pyautogui.leftClick(pos_x, pos_y)
                elif self.marks[row, col] == 1 and mark == 1:
                    pyautogui.leftClick(pos_x, pos_y)
