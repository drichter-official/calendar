import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class KingsRule(BaseRule):
    """
    Sudoku with King's Rule: No two cells that are adjacent (including diagonally)
    can contain the same digit.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "King's Rule"
        self.description = "No adjacent cells (including diagonals) can have the same digit"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the king's rule.
        """
        # Check all 8 surrounding cells (king's moves in chess)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if grid[nr][nc] == num:
                        return False

        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return KingsRule(size, box_size)

