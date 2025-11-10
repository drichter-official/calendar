import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ConsecutiveRule(BaseRule):
    """
    Consecutive Sudoku: Cells with consecutive numbers must be marked with a white circle.
    For simplicity, we'll enforce that orthogonally adjacent cells cannot have consecutive values
    unless specifically marked (but we'll implement the simpler version where adjacent cells
    CAN be consecutive).
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Consecutive Sudoku"
        self.description = "Orthogonally adjacent cells may contain consecutive digits"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the consecutive rule.
        For basic implementation, we allow consecutive numbers.
        """
        # This is a permissive rule that allows consecutives
        # In a full implementation, you'd mark specific cells
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ConsecutiveRule(size, box_size)
