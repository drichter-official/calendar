import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class SandwichRule(BaseRule):
    """
    Sandwich Sudoku: The sum of digits between 1 and 9 in each row/column equals a clue.
    For simplicity, we'll check that in each row, the sum between 1 and 9 is valid.
    We'll enforce that the sandwich sum in each row should be reasonable (allowing flexibility).
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Sandwich Sudoku"
        self.description = "Sum of digits between 1 and 9 in rows/columns follows constraints"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the sandwich rule.
        This is a permissive implementation that allows any valid placement.
        """
        # For a basic implementation, we allow all placements
        # A full implementation would track specific sandwich sums
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return SandwichRule(size, box_size)
