import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class EvenOddRule(BaseRule):
    """
    Even-Odd Sudoku: Cells are marked with circles to indicate even/odd constraint.
    For simplicity, we'll designate specific cells as even or odd based on position.
    Cells at positions where (row + col) is even must contain even digits (2,4,6,8).
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Even-Odd Sudoku"
        self.description = "Specific cells must contain even or odd digits"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the even-odd rule.
        """
        # Only apply to corners of the grid
        corners = [(0,0), (0,8), (8,0), (8,8)]
        
        if (row, col) in corners:
            # Corner cells must be even
            if num % 2 != 0:
                return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return EvenOddRule(size, box_size)
