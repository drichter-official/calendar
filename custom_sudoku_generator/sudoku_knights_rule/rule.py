import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class KnightsRule(BaseRule):
    """
    Sudoku with Knight's Rule: No two cells that are a chess knight's move apart
    can contain the same digit.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Knight's Rule"
        self.description = "No two cells a knight's move apart can contain the same digit"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the knight's rule.
        """
        # Knight's move positions relative to (row, col)
        knight_moves = [
            (-2, -1), (-2, +1), (-1, -2), (-1, +2),
            (+1, -2), (+1, +2), (+2, -1), (+2, +1)
        ]

        for dr, dc in knight_moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                if grid[nr][nc] == num:
                    return False

        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return KnightsRule(size, box_size)
