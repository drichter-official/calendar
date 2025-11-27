import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


# Define multiple fun patterns for even/odd cells
PATTERNS = {
    "checkerboard": {
        "name": "Checkerboard",
        "description": "Alternating even/odd pattern like a checkerboard",
        "even_cells": {
            (0, 0), (0, 4), (0, 8),
            (2, 2), (2, 6),
            (4, 0), (4, 4), (4, 8),
            (6, 2), (6, 6),
            (8, 0), (8, 4), (8, 8),
        },
        "odd_cells": {
            (0, 2), (0, 6),
            (2, 0), (2, 4), (2, 8),
            (4, 2), (4, 6),
            (6, 0), (6, 4), (6, 8),
            (8, 2), (8, 6),
        },
    },
    "diamond": {
        "name": "Diamond",
        "description": "Diamond shape pattern with even center and odd edges",
        "even_cells": {
            (0, 4),
            (1, 3), (1, 5),
            (2, 2), (2, 4), (2, 6),
            (3, 3), (3, 5),
            (4, 4),
        },
        "odd_cells": {
            (4, 0), (4, 8),
            (5, 1), (5, 7),
            (6, 2), (6, 6),
            (7, 3), (7, 5),
            (8, 4),
        },
    },
    "cross": {
        "name": "X Marks",
        "description": "X-shaped pattern with even and odd markers",
        "even_cells": {
            (0, 0), (1, 1), (2, 2),
            (6, 6), (7, 7), (8, 8),
        },
        "odd_cells": {
            (0, 8), (1, 7), (2, 6),
            (6, 2), (7, 1), (8, 0),
        },
    },
    "corners": {
        "name": "Four Corners",
        "description": "Even cells in corner boxes, odd cells in center",
        "even_cells": {
            (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2),
            (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8),
        },
        "odd_cells": {
            (3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5),
        },
    },
    "stripes": {
        "name": "Stripes",
        "description": "Alternating horizontal stripes of even and odd",
        "even_cells": {
            (0, 0), (0, 2), (0, 4), (0, 6), (0, 8),
            (4, 0), (4, 2), (4, 4), (4, 6), (4, 8),
            (8, 0), (8, 2), (8, 4), (8, 6), (8, 8),
        },
        "odd_cells": {
            (2, 0), (2, 2), (2, 4), (2, 6), (2, 8),
            (6, 0), (6, 2), (6, 4), (6, 6), (6, 8),
        },
    },
    "spiral": {
        "name": "Spiral",
        "description": "Spiral pattern from center outward",
        "even_cells": {
            (4, 4), (3, 5), (5, 3),
            (2, 6), (6, 2),
        },
        "odd_cells": {
            (3, 3), (5, 5),
            (2, 2), (6, 6),
        },
    },
}


class EvenOddRule(BaseRule):
    """
    Even-Odd Sudoku: Cells are marked with circles to indicate even/odd constraint.
    Gray circles indicate even digits, white circles indicate odd digits.
    Randomly selects from multiple fun patterns when generating a new puzzle.
    """

    def __init__(self, size=9, box_size=3, pattern_name=None):
        super().__init__(size, box_size)
        self.name = "Even-Odd Sudoku"
        self.description = "Specific cells must contain even or odd digits"

        # Select a random pattern if none specified
        if pattern_name is None:
            pattern_name = random.choice(list(PATTERNS.keys()))
        
        if pattern_name not in PATTERNS:
            pattern_name = "checkerboard"  # Default fallback
        
        self.pattern_name = pattern_name
        pattern = PATTERNS[pattern_name]
        
        # Update name and description to include pattern info
        self.name = f"Even-Odd Sudoku ({pattern['name']})"
        self.description = pattern['description']

        # Define even cells (gray circles)
        self.even_cells = pattern['even_cells'].copy()

        # Define odd cells (white circles)
        self.odd_cells = pattern['odd_cells'].copy()

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
        """Return metadata including even/odd cell markings and pattern info."""
        metadata = super().get_metadata()
        metadata['even_cells'] = list(self.even_cells)
        metadata['odd_cells'] = list(self.odd_cells)
        metadata['pattern_name'] = self.pattern_name
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3, pattern_name=None):
    return EvenOddRule(size, box_size, pattern_name)
