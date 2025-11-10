import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ArrowRule(BaseRule):
    """
    Arrow Sudoku: The sum of digits along an arrow must equal the digit in the circle.
    For simplicity, we'll define one arrow: circle at (0,0) with arrow cells at (0,1), (0,2).
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Arrow Sudoku"
        self.description = "Sum of arrow cells must equal the circle cell value"
        
        # Define arrows: (circle_cell, [arrow_cells])
        self.arrows = [
            ((0, 0), [(0, 1), (0, 2)]),
            ((8, 8), [(8, 7), (8, 6)]),
        ]

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the arrow rule.
        """
        for circle, arrow_cells in self.arrows:
            circle_r, circle_c = circle
            
            # If we're placing in the circle
            if (row, col) == circle:
                # Sum arrow cells
                arrow_sum = sum(grid[r][c] for r, c in arrow_cells if grid[r][c] != 0)
                # Check if all arrow cells are filled
                all_filled = all(grid[r][c] != 0 for r, c in arrow_cells)
                if all_filled and arrow_sum != num:
                    return False
            
            # If we're placing in an arrow cell
            if (row, col) in arrow_cells:
                circle_val = grid[circle_r][circle_c]
                if circle_val != 0:
                    # Calculate current sum including this number
                    current_sum = num
                    for r, c in arrow_cells:
                        if (r, c) != (row, col) and grid[r][c] != 0:
                            current_sum += grid[r][c]
                    
                    # Check if all arrow cells would be filled
                    filled_count = sum(1 for r, c in arrow_cells if grid[r][c] != 0 or (r, c) == (row, col))
                    if filled_count == len(arrow_cells) and current_sum != circle_val:
                        return False
        
        return True


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ArrowRule(size, box_size)
