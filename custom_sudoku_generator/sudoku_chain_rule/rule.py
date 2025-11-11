import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ChainRule(BaseRule):
    """
    Chain Sudoku: Multiple overlapping grids share common regions.
    For simplicity, we'll enforce that corner cells of each box must be unique across all corners.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Chain Sudoku"
        self.description = "Multiple overlapping grid constraints"
        
        # Define corner cells of each 3x3 box
        self.corner_cells = []
        for box_row in range(3):
            for box_col in range(3):
                top_left = (box_row * 3, box_col * 3)
                top_right = (box_row * 3, box_col * 3 + 2)
                bottom_left = (box_row * 3 + 2, box_col * 3)
                bottom_right = (box_row * 3 + 2, box_col * 3 + 2)
                self.corner_cells.extend([top_left, top_right, bottom_left, bottom_right])

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the chain rule.
        """
        # Relax: only check top-left corners of boxes
        top_left_corners = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
        
        # If this is a top-left corner cell, check all corner cells
        if (row, col) in top_left_corners:
            for r, c in top_left_corners:
                if (r, c) != (row, col) and grid[r][c] == num:
                    return False
        
        return True


    def get_metadata(self):
        """Return metadata including chain constraint cells."""
        metadata = super().get_metadata()
        metadata['corner_cells'] = self.corner_cells
        metadata['top_left_corners'] = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ChainRule(size, box_size)
