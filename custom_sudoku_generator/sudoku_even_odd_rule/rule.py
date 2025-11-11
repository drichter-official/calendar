import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class EvenOddRule(BaseRule):
    """
    Even-Odd Sudoku: Cells are marked with circles to indicate even/odd constraint.
    Gray circles indicate even digits, white circles indicate odd digits.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Even-Odd Sudoku"
        self.description = "Specific cells must contain even or odd digits"

        # Define even cells (gray circles)
        self.even_cells = {
            (0, 0), (0, 4), (0, 8),
            (2, 2), (2, 6),
            (4, 0), (4, 4), (4, 8),
            (6, 2), (6, 6),
            (8, 0), (8, 4), (8, 8),
        }

        # Define odd cells (white circles)
        self.odd_cells = {
            (0, 2), (0, 6),
            (2, 0), (2, 4), (2, 8),
            (4, 2), (4, 6),
            (6, 0), (6, 4), (6, 8),
            (8, 2), (8, 6),
        }

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the even-odd rule.
        """
        if (row, col) in self.even_cells:
            # Must be even (2, 4, 6, 8)
            if num % 2 != 0:
                return False
        elif (row, col) in self.odd_cells:
            # Must be odd (1, 3, 5, 7, 9)
            if num % 2 == 0:
                return False

        return True


    def get_metadata(self):
        """Return metadata including even/odd cell markings."""
        metadata = super().get_metadata()
        metadata['even_cells'] = list(self.even_cells)
        metadata['odd_cells'] = list(self.odd_cells)
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return EvenOddRule(size, box_size)
