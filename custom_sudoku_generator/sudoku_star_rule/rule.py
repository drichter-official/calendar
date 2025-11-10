import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class StarRule(BaseRule):
    """
    Star Sudoku: Cells forming a star pattern must follow special constraints.
    The star pattern cells are: center and points extending from center.
    Star cells: (4,4), (2,4), (6,4), (4,2), (4,6), (3,3), (3,5), (5,3), (5,5)
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Star Sudoku"
        self.description = "Cells in star pattern must contain unique digits"
        
        # Define star pattern cells
        self.star_cells = {
            (4, 4),  # Center
            (2, 4),  # Top
            (6, 4),  # Bottom
            (4, 2),  # Left
            (4, 6),  # Right
            (3, 3),  # Upper-left diagonal
            (3, 5),  # Upper-right diagonal
            (5, 3),  # Lower-left diagonal
            (5, 5),  # Lower-right diagonal
        }

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the star rule.
        """
        # If this cell is part of the star pattern
        if (row, col) in self.star_cells:
            # Check all other star cells for duplicates
            for r, c in self.star_cells:
                if (r, c) != (row, col) and grid[r][c] == num:
                    return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return StarRule(size, box_size)
