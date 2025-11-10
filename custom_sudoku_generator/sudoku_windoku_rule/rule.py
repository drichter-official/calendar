import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class WindokuRule(BaseRule):
    """
    Windoku Sudoku: In addition to regular Sudoku rules, four extra 3x3 regions
    (windoku windows) must also contain digits 1-9 without repetition.
    The windows are positioned at (1,1), (1,5), (5,1), and (5,5) as top-left corners.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Windoku"
        self.description = "Four extra 3x3 regions must contain digits 1-9"
        
        # Define the four windoku windows (top-left corners)
        self.windoku_windows = [
            (1, 1),  # Top-left window
            (1, 5),  # Top-right window
            (5, 1),  # Bottom-left window
            (5, 5),  # Bottom-right window
        ]

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the windoku rule.
        """
        # Check if the cell is in any of the windoku windows
        for window_row, window_col in self.windoku_windows:
            if window_row <= row < window_row + 3 and window_col <= col < window_col + 3:
                # Check all cells in this window
                for r in range(window_row, window_row + 3):
                    for c in range(window_col, window_col + 3):
                        if grid[r][c] == num:
                            return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return WindokuRule(size, box_size)
