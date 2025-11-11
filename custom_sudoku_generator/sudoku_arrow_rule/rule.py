import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ArrowRule(BaseRule):
    """
    Arrow Sudoku: The sum of digits along an arrow must equal the digit in the circle.
    Multiple arrows with varying lengths create interesting constraints.

    This rule supports REVERSE GENERATION where arrows are created from a complete solution.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Arrow Sudoku"
        self.description = "Sum of arrow cells must equal the circle cell value"
        
        # Define arrows: (circle_cell, [arrow_cells])
        # Will be derived from solution or predefined
        self.arrows = []

    def supports_reverse_generation(self):
        """Arrow Sudoku strongly benefits from reverse generation."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive arrows from a completed Sudoku solution.

        Strategy:
        1. Pick random circle cells with values that can be sums (4-9)
        2. Create arrow paths from those circles
        3. Ensure arrow sums equal circle values
        """
        print("  Deriving arrows from solution...")

        self.arrows = []
        used_cells = set()

        # Try to create multiple arrows
        num_arrows = random.randint(4, 8)
        attempts = 0
        max_attempts = 100

        while len(self.arrows) < num_arrows and attempts < max_attempts:
            attempts += 1

            # Pick a random circle cell (prefer higher values for interesting sums)
            available_circles = [
                (r, c) for r in range(self.size) for c in range(self.size)
                if (r, c) not in used_cells and solution_grid[r][c] >= 4
            ]

            if not available_circles:
                break

            circle = random.choice(available_circles)
            target_sum = solution_grid[circle[0]][circle[1]]

            # Create an arrow path that sums to target
            arrow_cells = self._create_arrow_path(circle, target_sum, solution_grid, used_cells)

            if len(arrow_cells) >= 2:
                self.arrows.append((circle, arrow_cells))
                used_cells.add(circle)
                for cell in arrow_cells:
                    used_cells.add(cell)

        print(f"  Created {len(self.arrows)} arrows")

        return len(self.arrows) > 0

    def _create_arrow_path(self, circle, target_sum, solution_grid, used_cells):
        """
        Create an arrow path from circle that sums to target_sum.
        """
        arrow_cells = []
        current_sum = 0
        current_pos = circle

        # Try to build a path that reaches the target sum
        for _ in range(6):  # Max arrow length
            if current_sum >= target_sum:
                break

            # Find adjacent cells
            r, c = current_pos
            neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

            valid_neighbors = [
                (nr, nc) for nr, nc in neighbors
                if 0 <= nr < self.size and 0 <= nc < self.size
                and (nr, nc) not in used_cells
                and (nr, nc) not in arrow_cells
                and (nr, nc) != circle
            ]

            if not valid_neighbors:
                break

            # Pick neighbor that gets us closer to target
            best_neighbor = None
            for neighbor in valid_neighbors:
                val = solution_grid[neighbor[0]][neighbor[1]]
                if current_sum + val <= target_sum:
                    if best_neighbor is None or abs(target_sum - (current_sum + val)) < abs(target_sum - (current_sum + solution_grid[best_neighbor[0]][best_neighbor[1]])):
                        best_neighbor = neighbor

            if best_neighbor:
                arrow_cells.append(best_neighbor)
                current_sum += solution_grid[best_neighbor[0]][best_neighbor[1]]
                current_pos = best_neighbor

                if current_sum == target_sum:
                    return arrow_cells
            else:
                break

        # Only return if we hit the target exactly
        if current_sum == target_sum and len(arrow_cells) >= 2:
            return arrow_cells
        return []

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


    def get_metadata(self):
        """Return metadata including arrow configurations."""
        metadata = super().get_metadata()
        metadata['arrows'] = [
            {
                'circle': circle,
                'arrow_cells': arrow_cells
            }
            for circle, arrow_cells in self.arrows
        ]
        metadata['generation_mode'] = 'reverse' if len(self.arrows) > 3 else 'forward'
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ArrowRule(size, box_size)
