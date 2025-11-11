import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class KropkiRule(BaseRule):
    """
    Kropki Sudoku: White dots between cells mean they differ by 1,
    black dots mean one is double the other.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Kropki Sudoku"
        self.description = "Adjacent cells have specific difference or ratio relationships"

        # Define white dots (consecutive, differ by 1): pairs of cells
        self.white_dots = [
            ((0, 1), (0, 2)),
            ((1, 0), (2, 0)),
            ((2, 3), (2, 4)),
            ((3, 5), (3, 6)),
            ((4, 2), (5, 2)),
            ((5, 7), (6, 7)),
            ((7, 4), (7, 5)),
        ]

        # Define black dots (ratio 1:2): pairs of cells
        self.black_dots = [
            ((0, 3), (0, 4)),
            ((1, 6), (2, 6)),
            ((3, 1), (3, 2)),
            ((4, 4), (4, 5)),
            ((6, 0), (7, 0)),
            ((7, 7), (8, 7)),
        ]

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the kropki rule.
        """
        # Check white dots (differ by 1)
        for cell1, cell2 in self.white_dots:
            r1, c1 = cell1
            r2, c2 = cell2

            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0 and abs(num - val2) != 1:
                    return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0 and abs(val1 - num) != 1:
                    return False

        # Check black dots (ratio 1:2)
        for cell1, cell2 in self.black_dots:
            r1, c1 = cell1
            r2, c2 = cell2

            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0 and not (num * 2 == val2 or val2 * 2 == num):
                    return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0 and not (val1 * 2 == num or num * 2 == val1):
                    return False

        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return KropkiRule(size, box_size)
