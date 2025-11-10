import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ArgyleRule(BaseRule):
    """
    Argyle Sudoku: Diagonals of 3x3 boxes must not contain repeated digits.
    Each 3x3 box has two main diagonals that cannot have repeated values.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Argyle Sudoku"
        self.description = "Diagonals of 3x3 boxes must not contain repeated digits"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the argyle rule.
        """
        # Determine which 3x3 box this cell belongs to
        box_row = (row // self.box_size) * self.box_size
        box_col = (col // self.box_size) * self.box_size
        
        # Position within the box
        in_box_row = row - box_row
        in_box_col = col - box_col
        
        # Check main diagonal of the box (top-left to bottom-right)
        if in_box_row == in_box_col:
            for i in range(self.box_size):
                if grid[box_row + i][box_col + i] == num:
                    return False
        
        # Check anti-diagonal of the box (top-right to bottom-left)
        if in_box_row + in_box_col == self.box_size - 1:
            for i in range(self.box_size):
                if grid[box_row + i][box_col + (self.box_size - 1 - i)] == num:
                    return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ArgyleRule(size, box_size)
