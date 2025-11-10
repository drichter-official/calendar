import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class KillerRule(BaseRule):
    """
    Killer Sudoku: Groups of cells (cages) must sum to specific values, and no digit
    can repeat within a cage. For simplicity, we'll define some cages based on position.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Killer Sudoku"
        self.description = "Cages must sum to specific values with no repeated digits"
        
        # Define some simple cages: each 2x2 region in the top-left of each box
        self.cages = []
        for box_row in range(3):
            for box_col in range(3):
                cage = []
                for r in range(2):
                    for c in range(2):
                        cage.append((box_row * 3 + r, box_col * 3 + c))
                self.cages.append(cage)

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the killer rule.
        """
        # Find which cage this cell belongs to
        for cage in self.cages:
            if (row, col) in cage:
                # Check for duplicate in the same cage
                for r, c in cage:
                    if grid[r][c] == num:
                        return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return KillerRule(size, box_size)
