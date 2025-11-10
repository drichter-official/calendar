import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ThermoRule(BaseRule):
    """
    Thermo Sudoku: Digits must strictly increase along thermometer lines.
    For simplicity, we'll define the main diagonal as a thermometer.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Thermo Sudoku"
        self.description = "Digits strictly increase along thermometer lines"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the thermo rule.
        Only first 3 cells of main diagonal form a thermometer.
        """
        # Apply thermo rule to first 3 cells of main diagonal only
        if row == col and row < 3:
            # Check previous cell on diagonal (should be less)
            if row > 0:
                prev_num = grid[row - 1][col - 1]
                if prev_num != 0 and prev_num >= num:
                    return False
            # Check next cell on diagonal (should be greater)
            if row < 2:
                next_num = grid[row + 1][col + 1]
                if next_num != 0 and next_num <= num:
                    return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ThermoRule(size, box_size)
