import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class AsteriskRule(BaseRule):
    """
    Asterisk Sudoku: Nine cells forming an asterisk pattern must contain digits 1-9.
    The asterisk is centered at (4,4) with arms extending outward.
    Cells: (1,4), (2,2), (2,6), (4,1), (4,4), (4,7), (6,2), (6,6), (7,4)
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Asterisk Sudoku"
        self.description = "Nine cells forming an asterisk must contain digits 1-9"
        
        # Define the asterisk cells (0-indexed)
        self.asterisk_cells = {
            (1, 4),  # Top
            (2, 2),  # Upper-left
            (2, 6),  # Upper-right
            (4, 1),  # Left
            (4, 4),  # Center
            (4, 7),  # Right
            (6, 2),  # Lower-left
            (6, 6),  # Lower-right
            (7, 4),  # Bottom
        }

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the asterisk rule.
        """
        # If this cell is part of the asterisk, check all asterisk cells
        if (row, col) in self.asterisk_cells:
            for r, c in self.asterisk_cells:
                if grid[r][c] == num:
                    return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return AsteriskRule(size, box_size)
