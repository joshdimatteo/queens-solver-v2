from puzzle import Puzzle
import numpy as np

class Solver:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle

    # Loops below methods to solve
    def solve(self, cap=5):
        count = 0
        while not self.puzzle.is_solved() and count < cap:
            self.color_line_search()
            self.mark_line_search()
            count += 1

    # Searches columns or rows for marks
    def mark_line_count(self, index, orient, mark):
        if orient.lower() == "x":
            arr = self.puzzle.marks[index]
        elif orient.lower() == "y":
            arr = self.puzzle.marks[:, index]
        else:
            raise ValueError(f"Unknown Orientation: {orient}")

        unique, count = np.unique(arr, return_counts=True)
        if mark in unique:
            return dict(zip(unique, count))[mark]
        return 0

    # Counts how much of a color remains
    def color_count(self, color):
        counter = 0
        for row in range(self.puzzle.size):
            for col in range(self.puzzle.size):
                if self.puzzle.marks[row, col] == 0 and self.puzzle.colors[row, col] == color:
                    counter += 1
        return counter



    # Type 1: Searching marks

    # 1. Search rows/cols for marks that are either
    # [X] [X] [ ] [X] [X]
    # [X] [X] [ ] [ ] [X]
    # [X] [ ] [ ] [ ] [X]
    # [X] [ ] [X] [ ] [X]
    def mark_line_search(self):

        # Search rows
        for row in range(self.puzzle.size):
            mark_count = self.mark_line_count(row, "x", 0)

            # If there is only one open spot, find it and place a queen
            if mark_count == 1:
                print(f"[ ] Found: {row}, {np.where(self.puzzle.marks[row] == 0)[0][0]}")
                self.puzzle.mark((np.where(self.puzzle.marks[row] == 0)[0][0], row), 2)

            # If there are two open spots
            elif mark_count == 2:

                # Iterate over the row and check for [ ] [ ]
                for n in range(self.puzzle.size - 1):
                    if self.puzzle.marks[row, n] + self.puzzle.marks[row, n+1] == 0:
                        print(f"[ ] [ ] Found: {row}, {n}")

                        # Marks spots to the sides
                        self.puzzle.mark((row-1, n), 1)
                        self.puzzle.mark((row-1, n+1), 1)
                        self.puzzle.mark((row+1, n), 1)
                        self.puzzle.mark((row+1, n+1), 1)

                # Iterate over the row and check for [ ] [x] [ ]
                for n in range(self.puzzle.size - 2):
                    if self.puzzle.marks[row, n] + self.puzzle.marks[row, n+2] == 0:
                        print(f"[ ] [x] [ ] Found: {row}, {n}")

                        # Marks spots to the sides
                        self.puzzle.mark((row-1, n+1), 1)
                        self.puzzle.mark((row+1, n+1), 1)

            # If there are 3 open spots
            elif mark_count == 3:

                # Iterate over the row and check for [ ] [ ] [ ]
                for n in range(self.puzzle.size - 2):
                    if self.puzzle.marks[row, n] + + self.puzzle.marks[row, n+1] + self.puzzle.marks[row, n+2] == 0:
                        print(f"[ ] [ ] [ ] Found: {row}, {n}")

                        # Marks spots to the sides
                        self.puzzle.mark((row - 1, n + 1), 1)
                        self.puzzle.mark((row + 1, n + 1), 1)

        # Search columns
        for col in range(self.puzzle.size):
            mark_count = self.mark_line_count(col, "y", 0)

            # If there is only one open spot, find it and place a queen
            if mark_count == 1:
                print(f"[ ] Found: {np.where(self.puzzle.marks[:, col] == 0)[0][0]}, {col}")
                self.puzzle.mark((col, np.where(self.puzzle.marks[:, col] == 0)[0][0]), 2)

            # If there are two open spots
            elif mark_count == 2:

                # Iterate over the row and check for [ ] [ ]
                for n in range(self.puzzle.size - 1):
                    if self.puzzle.marks[n, col] + self.puzzle.marks[n+1, col] == 0:
                        print(f"[ ] [ ] Vertical Found: {n}, {col}")

                        self.puzzle.mark((n, col - 1), 1)
                        self.puzzle.mark((n + 1, col - 1), 1)
                        self.puzzle.mark((n, col + 1), 1)
                        self.puzzle.mark((n + 1, col + 1), 1)

                # Iterate over the row and check for [ ] [x] [ ]
                for n in range(self.puzzle.size - 2):
                    if self.puzzle.marks[n, col] + self.puzzle.marks[n+2, col] == 0:
                        print(f"[ ] [x] [ ] Vertical Found: {n}, {col}")

                        # Marks spots to the sides
                        self.puzzle.mark((n + 1, col + 1), 1)
                        self.puzzle.mark((n + 1, col - 1), 1)

            # If there are 3 open spots
            elif mark_count == 3:

                # Iterate over the row and check for [ ] [ ] [ ]
                for n in range(self.puzzle.size - 2):
                    if self.puzzle.marks[n, col] + self.puzzle.marks[n+1, col] + self.puzzle.marks[n+2, col] == 0:
                        print(f"[ ] [ ] [ ] Vertical Found: {n}, {col}")

                        # Marks spots to the sides
                        self.puzzle.mark((n + 1, col + 1), 1)
                        self.puzzle.mark((n + 1, col - 1), 1)

    # Type 2: Searching colors

    # 1. Searches for if a color is entirely contained in a single line
    def color_line_search(self):

        # Check each color
        for color_id in range(self.puzzle.size):
            total = self.color_count(color_id)

            # Check each row
            for row in range(self.puzzle.size):
                row_counter = 0

                for col in range(self.puzzle.size):
                    if self.puzzle.colors[row, col] == color_id and self.puzzle.marks[row, col] == 0:
                        row_counter += 1

                if row_counter == total != 0:
                    print(f"Row Found: {row}")

                    for col in range(self.puzzle.size):
                        if self.puzzle.colors[row, col] != color_id:
                            self.puzzle.mark((row, col), 1)

            # Check each column
            for col in range(self.puzzle.size):
                col_counter = 0

                for row in range(self.puzzle.size):
                    if self.puzzle.colors[row, col] == color_id and self.puzzle.marks[row, col] == 0:
                        col_counter += 1

                if col_counter == total != 0:
                    print(f"Column Found: {col}")

                    for row in range(self.puzzle.size):
                        if self.puzzle.colors[row, col] != color_id:
                            self.puzzle.mark((row, col), 1)
