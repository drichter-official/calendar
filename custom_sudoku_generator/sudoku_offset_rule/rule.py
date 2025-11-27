import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class OffsetRule(BaseRule):
    """
    Offset Sudoku: The grid contains 9 groups of cells, where each group has the same
    relative positions within their respective 3x3 boxes. Each group must contain
    digits 1-9 exactly once.

    For example, all top-left cells of each 3x3 box form one group, all top-center
    cells form another group, etc. This creates 9 groups of 9 cells each.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Offset Sudoku"
        self.description = "Cells at same positions within each 3x3 box must contain digits 1-9"

        # Define the 9 offset groups (one for each position within a 3x3 box).
        # Each group contains 9 cells - one from each 3x3 box at the same relative position.
        #
        # Group 0: All top-left cells (position 0,0 within each box)
        # Group 1: All top-center cells (position 0,1 within each box)
        # Group 2: All top-right cells (position 0,2 within each box)
        # Group 3: All middle-left cells (position 1,0 within each box)
        # Group 4: All center cells (position 1,1 within each box)
        # Group 5: All middle-right cells (position 1,2 within each box)
        # Group 6: All bottom-left cells (position 2,0 within each box)
        # Group 7: All bottom-center cells (position 2,1 within each box)
        # Group 8: All bottom-right cells (position 2,2 within each box)
        self.offset_groups = []
        for offset_row in range(3):
            for offset_col in range(3):
                group = []
                for box_row in range(3):
                    for box_col in range(3):
                        row = box_row * 3 + offset_row
                        col = box_col * 3 + offset_col
                        group.append((row, col))
                self.offset_groups.append(group)

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the offset rule.
        """
        # Find which offset group this cell belongs to
        offset_row = row % 3
        offset_col = col % 3
        group_index = offset_row * 3 + offset_col

        # Check all cells in this offset group
        for cell_row, cell_col in self.offset_groups[group_index]:
            if (cell_row, cell_col) != (row, col) and grid[cell_row][cell_col] == num:
                return False

        return True

    def get_metadata(self):
        """Return metadata including offset group information."""
        metadata = super().get_metadata()
        metadata['offset_groups'] = [
            [[r, c] for r, c in group]
            for group in self.offset_groups
        ]
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return OffsetRule(size, box_size)
