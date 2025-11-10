import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class WhisperRule(BaseRule):
    """
    Whisper Sudoku: Adjacent cells along whisper lines must differ by at least 5.
    For simplicity, we'll apply this to the center column.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Whisper Sudoku"
        self.description = "Adjacent cells along whisper lines differ by at least 5"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the whisper rule.
        Only first 3 cells of center column form a whisper line.
        """
        # Apply whisper rule to first 3 cells of center column only
        if col == 4 and row < 3:
            # Check above
            if row > 0:
                above_num = grid[row - 1][col]
                if above_num != 0 and abs(num - above_num) < 5:
                    return False
            # Check below
            if row < 2:
                below_num = grid[row + 1][col]
                if below_num != 0 and abs(num - below_num) < 5:
                    return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return WhisperRule(size, box_size)
