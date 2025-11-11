import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class XVRule(BaseRule):
    """
    XV Sudoku: Cells separated by an X must sum to 10, cells separated by a V must sum to 5.
    Multiple X and V markers create interesting constraint patterns.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "XV Sudoku"
        self.description = "Specific adjacent cells must sum to 10 (X) or 5 (V)"

        # Define X markers (sum to 10): pairs of cells
        self.x_pairs = [
            ((0, 0), (0, 1)),
            ((0, 4), (0, 5)),
            ((1, 2), (1, 3)),
            ((2, 6), (2, 7)),
            ((3, 1), (4, 1)),
            ((5, 3), (5, 4)),
            ((6, 5), (7, 5)),
            ((8, 2), (8, 3)),
        ]

        # Define V markers (sum to 5): pairs of cells
        self.v_pairs = [
            ((0, 2), (0, 3)),
            ((1, 5), (1, 6)),
            ((2, 0), (3, 0)),
            ((4, 4), (4, 5)),
            ((5, 7), (6, 7)),
            ((7, 1), (7, 2)),
            ((8, 6), (8, 7)),
        ]

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the XV rule.
        """
        # Check X pairs (sum to 10)
        for cell1, cell2 in self.x_pairs:
            r1, c1 = cell1
            r2, c2 = cell2

            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0 and num + val2 != 10:
                    return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0 and val1 + num != 10:
                    return False

        # Check V pairs (sum to 5)
        for cell1, cell2 in self.v_pairs:
            r1, c1 = cell1
            r2, c2 = cell2

            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0 and num + val2 != 5:
                    return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0 and val1 + num != 5:
                    return False

        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return XVRule(size, box_size)
