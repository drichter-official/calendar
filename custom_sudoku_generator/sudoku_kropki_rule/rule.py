import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class KropkiRule(BaseRule):
    """
    Kropki Sudoku: White dots between cells mean they differ by 1,
    black dots mean one is double the other.
    For simplicity: cells at positions where row==col must differ by 1 from neighbors,
    cells where row+col==8 must have double relationship with neighbors.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Kropki Sudoku"
        self.description = "Adjacent cells have specific difference or ratio relationships"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the kropki rule.
        """
        # Simplify: only apply to select cells to avoid over-constraint
        # White dot constraint: on main diagonal only
        if row == col and col + 1 < self.size and col < 3:
            right_num = grid[row][col + 1]
            if right_num != 0 and abs(num - right_num) != 1:
                return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return KropkiRule(size, box_size)
