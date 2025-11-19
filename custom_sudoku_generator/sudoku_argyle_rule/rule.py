import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ArgyleRule(BaseRule):
    """
    Argyle Sudoku: No repeated digits on 8 offset diagonals that form an argyle pattern.
    The diagonals are offset to create a diamond/argyle pattern across the grid.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Argyle Sudoku"
        self.description = ("No repeated digits on marked diagonals")

        # Define the 8 argyle diagonals
        # 4 diagonals going down-right (/)
        self.argyle_diagonals = [
            #[
            # Down-right diagonals starting from column 1, 3, 5, 7
                [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)],  # col 1
                [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7)],  # col -1
                # Down-left diagonals (\) starting from column 7, 5, 3, 1
                [(0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)],  # col 7
                [(1, 8), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3), (7, 2), (8, 1)],  # col -7
            #],
            #[
            #    [(0, 4), (1, 5), (2, 6), (3, 7), (4, 8)],
            #    [(4, 0), (5, 1), (6, 2), (7, 3), (8, 4)],
            #    [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)],
            #    [(4, 8), (5, 7), (6, 6), (7, 5), (8, 4)],
            #]
        ]

        # Create a mapping from (row, col) to list of diagonal indices
        self.cell_to_diagonals = {}
        for diag_idx, diagonal in enumerate(self.argyle_diagonals):
            for cell in diagonal:
                if cell not in self.cell_to_diagonals:
                    self.cell_to_diagonals[cell] = []
                self.cell_to_diagonals[cell].append(diag_idx)

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the argyle rule.
        """
        cell = (row, col)

        # If this cell is not on any argyle diagonal, no constraint
        if cell not in self.cell_to_diagonals:
            return True

        # Check each diagonal this cell belongs to
        for diag_idx in self.cell_to_diagonals[cell]:
            diagonal = self.argyle_diagonals[diag_idx]
            for r, c in diagonal:
                if grid[r][c] == num:
                    return False
        
        return True

    def get_metadata(self):
        """Return metadata including argyle diagonal cells."""
        metadata = super().get_metadata()
        
        # All cells that are part of any argyle diagonal
        argyle_cells = list(self.cell_to_diagonals.keys())
        metadata['argyle_cells'] = argyle_cells
        metadata['argyle_diagonals'] = self.argyle_diagonals
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ArgyleRule(size, box_size)
