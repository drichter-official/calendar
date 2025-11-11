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
    Multiple whisper lines create interesting constraint patterns.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Whisper Sudoku"
        self.description = "Adjacent cells along whisper lines differ by at least 5"

        # Define whisper lines (lists of cells where adjacent pairs differ by at least 5)
        self.whisper_lines = [
            [(0, 1), (1, 1), (2, 1), (3, 1)],  # Vertical line
            [(1, 4), (2, 4), (3, 4)],  # Vertical line
            [(4, 0), (4, 1), (4, 2)],  # Horizontal line
            [(5, 5), (6, 5), (7, 5)],  # Vertical line
            [(7, 7), (8, 7), (8, 6)],  # L-shaped line
        ]

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the whisper rule.
        """
        # Check each whisper line
        for line in self.whisper_lines:
            if (row, col) in line:
                idx = line.index((row, col))

                # Check previous cell in line (must differ by at least 5)
                if idx > 0:
                    prev_r, prev_c = line[idx - 1]
                    prev_num = grid[prev_r][prev_c]
                    if prev_num != 0 and abs(num - prev_num) < 5:
                        return False

                # Check next cell in line (must differ by at least 5)
                if idx < len(line) - 1:
                    next_r, next_c = line[idx + 1]
                    next_num = grid[next_r][next_c]
                    if next_num != 0 and abs(num - next_num) < 5:
                        return False

        return True


    def get_metadata(self):
        """Return metadata including whisper lines."""
        metadata = super().get_metadata()
        metadata['whisper_lines'] = self.whisper_lines
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return WhisperRule(size, box_size)
