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
    Multiple renban lines create interesting constraint patterns.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Renban Sudoku"
        self.description = "Specific lines must contain consecutive digits in any order"

        # Define renban lines (lists of cells that must contain consecutive digits)
        self.renban_lines = [
            [(0, 0), (0, 1), (0, 2), (0, 3)],  # Horizontal line
            [(2, 2), (3, 2), (4, 2)],  # Vertical line
            [(1, 5), (1, 6), (1, 7)],  # Horizontal line
            [(4, 4), (5, 5), (6, 6)],  # Diagonal line
            [(7, 0), (7, 1), (7, 2), (7, 3)],  # Horizontal line
            [(8, 5), (8, 6), (8, 7)],  # Horizontal line
        ]

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the renban rule.
        """
        # Check each renban line
        for line in self.renban_lines:
            if (row, col) in line:
                # Get all filled values in this line (including current)
                values = []
                for r, c in line:
                    if (r, c) == (row, col):
                        values.append(num)
                    elif grid[r][c] != 0:
                        values.append(grid[r][c])

                # If more than one value, check if they form a consecutive sequence
                if len(values) > 1:
                    sorted_vals = sorted(values)
                    for i in range(len(sorted_vals) - 1):
                        if sorted_vals[i + 1] - sorted_vals[i] != 1:
                            return False

                    # Also check if we can fit remaining values
                    # The range must be able to fit in the line length
                    if len(values) == len(line):
                        expected_range = sorted_vals[-1] - sorted_vals[0] + 1
                        if expected_range != len(line):
                            return False

        return True


    def get_metadata(self):
        """Return metadata including renban lines."""
        metadata = super().get_metadata()
        metadata['renban_lines'] = self.renban_lines
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return RenbanRule(size, box_size)
