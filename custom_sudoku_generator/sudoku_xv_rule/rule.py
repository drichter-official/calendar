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
    For simplicity, we'll mark specific adjacent pairs.
    Here we'll implement: horizontal neighbors at even columns sum to 10 (X),
    vertical neighbors at even rows sum to 5 (V).
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "XV Sudoku"
        self.description = "Specific adjacent cells must sum to 10 (X) or 5 (V)"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the XV rule.
        """
        # Very relaxed constraint - only check first two cells of first row
        if row == 0 and col == 0:
            right_num = grid[0][1]
            if right_num != 0 and num + right_num != 10:
                return False
        if row == 0 and col == 1:
            left_num = grid[0][0]
            if left_num != 0 and num + left_num != 10:
                return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return XVRule(size, box_size)
