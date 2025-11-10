import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class SkyscraperRule(BaseRule):
    """
    Skyscraper Sudoku: Clues around the edge indicate how many "buildings" (digits) are visible
    when looking into that row/column. For simplicity, we allow any valid placement.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Skyscraper Sudoku"
        self.description = "Visibility clues around edges indicate visible buildings"

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the skyscraper rule.
        For a basic implementation, we allow all placements.
        """
        # Full implementation would check visibility constraints
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return SkyscraperRule(size, box_size)
