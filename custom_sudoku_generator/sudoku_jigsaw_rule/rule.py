import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class JigsawRule(BaseRule):
    """
    Jigsaw Sudoku: Instead of regular 3x3 boxes, the grid is divided into irregular regions.
    For simplicity, we'll define custom regions that are non-standard shapes.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Jigsaw Sudoku"
        self.description = "Irregular regions instead of standard 3x3 boxes"
        
        # Define custom jigsaw regions (9 regions, each with 9 cells)
        # This is a simplified version with somewhat irregular shapes
        self.jigsaw_regions = [
            # Region 0
            [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)],
            # Region 1
            [(0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)],
            # Region 2
            [(0,6), (0,7), (0,8), (1,6), (1,7), (1,8), (2,6), (2,7), (2,8)],
            # Region 3
            [(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)],
            # Region 4
            [(3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5)],
            # Region 5
            [(3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8)],
            # Region 6
            [(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)],
            # Region 7
            [(6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5)],
            # Region 8
            [(6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)],
        ]

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the jigsaw rule.
        """
        # Find which region this cell belongs to
        for region in self.jigsaw_regions:
            if (row, col) in region:
                # Check for duplicates in this region
                for r, c in region:
                    if grid[r][c] == num:
                        return False
                break
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return JigsawRule(size, box_size)
