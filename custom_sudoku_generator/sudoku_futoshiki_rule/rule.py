import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class FutoshikiRule(BaseRule):
    """
    Futoshiki Sudoku: Inequality signs between cells indicate greater/less than relationships.
    For simplicity, we'll enforce that cells increase from left to right in the first row.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Futoshiki Sudoku"
        self.description = "Inequality constraints between adjacent cells"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the futoshiki rule.
        First three cells of first row must be increasing.
        """
        # Apply inequality constraint to first 3 cells of first row only
        if row == 0 and col < 3:
            # Check left neighbor (should be less)
            if col > 0:
                left_num = grid[row][col - 1]
                if left_num != 0 and left_num >= num:
                    return False
            # Check right neighbor (should be greater)
            if col < 2:
                right_num = grid[row][col + 1]
                if right_num != 0 and right_num <= num:
                    return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return FutoshikiRule(size, box_size)
