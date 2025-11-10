import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class CenterDotRule(BaseRule):
    """
    Center Dot Sudoku: The center cell of each 3x3 box must follow a special constraint.
    All center cells (at positions (1,1), (1,4), (1,7), (4,1), (4,4), (4,7), (7,1), (7,4), (7,7))
    must contain different digits.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Center Dot Sudoku"
        self.description = "Center cells of all 3x3 boxes must contain unique digits"
        
        # Define the center cells of each 3x3 box (0-indexed)
        self.center_cells = {
            (1, 1), (1, 4), (1, 7),
            (4, 1), (4, 4), (4, 7),
            (7, 1), (7, 4), (7, 7),
        }

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the center dot rule.
        """
        # If this cell is a center cell, check all other center cells
        if (row, col) in self.center_cells:
            for r, c in self.center_cells:
                if grid[r][c] == num:
                    return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return CenterDotRule(size, box_size)
