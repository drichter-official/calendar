import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class DiagonalRule(BaseRule):
    """
    Sudoku with Diagonal Rule (also known as Sudoku X):
    The main diagonals must also contain all digits 1-9 without repetition.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Diagonal Rule (Sudoku X)"
        self.description = "Main diagonals must contain each digit 1-9 exactly once"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the diagonal rule.
        """
        # Check main diagonal (top-left to bottom-right)
        if row == col:
            for i in range(self.size):
                if grid[i][i] == num:
                    return False

        # Check anti-diagonal (top-right to bottom-left)
        if row + col == self.size - 1:
            for i in range(self.size):
                if grid[i][self.size - 1 - i] == num:
                    return False

        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return DiagonalRule(size, box_size)

