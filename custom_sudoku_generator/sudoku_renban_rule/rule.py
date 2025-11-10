import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class RenbanRule(BaseRule):
    """
    Renban Sudoku: Cells along renban lines must contain consecutive digits in any order.
    For simplicity, we'll designate the first row as a renban line.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Renban Sudoku"
        self.description = "Specific lines must contain consecutive digits in any order"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the renban rule.
        First three cells of first row must have consecutive digits.
        """
        # Apply renban constraint to first three cells of first row only
        if row == 0 and col < 3:
            # Count non-zero values in first 3 cells
            values = [grid[0][c] for c in range(3) if grid[0][c] != 0]
            if (row, col) == (0, col) and num not in values:
                values.append(num)
            
            if len(values) > 1:
                # Check if all values form a consecutive sequence
                sorted_vals = sorted(values)
                for i in range(len(sorted_vals) - 1):
                    if sorted_vals[i + 1] - sorted_vals[i] != 1:
                        return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return RenbanRule(size, box_size)
