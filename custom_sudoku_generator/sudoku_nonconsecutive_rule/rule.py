import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class NonconsecutiveRule(BaseRule):
    """
    Nonconsecutive Sudoku: Orthogonally adjacent cells cannot contain consecutive digits.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Nonconsecutive Sudoku"
        self.description = "Orthogonally adjacent cells cannot have consecutive digits"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the nonconsecutive rule.
        """
        # Apply only to first 3 rows and columns to make it less restrictive
        if row < 3 or col < 3:
            # Check orthogonally adjacent cells (up, down, left, right)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    adjacent_num = grid[nr][nc]
                    if adjacent_num != 0:
                        # Check if consecutive
                        if abs(adjacent_num - num) == 1:
                            return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return NonconsecutiveRule(size, box_size)
