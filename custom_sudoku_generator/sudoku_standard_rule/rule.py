import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class StandardRule(BaseRule):
    """
    Standard Sudoku: Only standard row, column, and box constraints apply.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Standard Sudoku"
        self.description = "Fill in the grid so every row, column, and 3x3 box contains the digits 1-9"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) is valid.
        For standard sudoku, no additional constraints beyond base rules.
        """
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return StandardRule(size, box_size)
