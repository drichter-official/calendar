import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class SandwichRule(BaseRule):
    """
    Sandwich Sudoku: The sum of digits between 1 and 9 in each row/column equals a clue.
    Clues are given for specific rows and columns.

    This rule supports REVERSE GENERATION where sandwich sums are calculated from
    a complete solution, ensuring valid and solvable puzzles.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Sandwich Sudoku"
        self.description = "Sum of digits between 1 and 9 in rows/columns equals given clues"

        # Define sandwich clues: {('row', index): sum, ('col', index): sum}
        self.sandwich_clues = {}

    def supports_reverse_generation(self):
        """Sandwich Sudoku strongly benefits from reverse generation."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive sandwich clues from a completed Sudoku solution.

        Strategy:
        1. Calculate sandwich sums for all rows and columns
        2. Select a subset of interesting clues (not too easy, not trivial)
        3. Ensure good distribution across the grid
        """
        print("  Deriving sandwich clues from solution...")

        self.sandwich_clues = {}

        # Calculate all possible sandwich sums
        candidates = []

        # Rows
        for r in range(self.size):
            pos_1 = None
            pos_9 = None
            for c in range(self.size):
                if solution_grid[r][c] == 1:
                    pos_1 = c
                elif solution_grid[r][c] == 9:
                    pos_9 = c

            if pos_1 is not None and pos_9 is not None:
                start = min(pos_1, pos_9) + 1
                end = max(pos_1, pos_9)
                sandwich_sum = sum(solution_grid[r][c] for c in range(start, end))
                # Only include interesting sums (not 0, and not too high)
                if sandwich_sum > 0:
                    candidates.append(('row', r, sandwich_sum))

        # Columns
        for c in range(self.size):
            pos_1 = None
            pos_9 = None
            for r in range(self.size):
                if solution_grid[r][c] == 1:
                    pos_1 = r
                elif solution_grid[r][c] == 9:
                    pos_9 = r

            if pos_1 is not None and pos_9 is not None:
                start = min(pos_1, pos_9) + 1
                end = max(pos_1, pos_9)
                sandwich_sum = sum(solution_grid[r][c] for r in range(start, end))
                # Only include interesting sums (not 0, and not too high)
                if sandwich_sum > 0:
                    candidates.append(('col', c, sandwich_sum))

        # Select a diverse subset of clues (at least 10, up to 70% of available)
        if len(candidates) > 0:
            # Ensure at least 10 clues if possible, otherwise use all available
            min_clues = min(10, len(candidates))
            max_clues = max(min_clues, int(len(candidates) * 0.7))
            num_clues = random.randint(min_clues, max_clues)
            selected = random.sample(candidates, num_clues)

            for direction, index, sandwich_sum in selected:
                self.sandwich_clues[(direction, index)] = sandwich_sum

        print(f"  Created {len(self.sandwich_clues)} sandwich clues")

        return len(self.sandwich_clues) > 0

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the sandwich rule.
        """
        # Check row constraint if this row has a sandwich clue
        if ('row', row) in self.sandwich_clues:
            target_sum = self.sandwich_clues[('row', row)]

            # Find positions of 1 and 9 in this row
            pos_1 = None
            pos_9 = None
            for c in range(self.size):
                val = grid[row][c] if (row, c) != (row, col) else num
                if val == 1:
                    pos_1 = c
                elif val == 9:
                    pos_9 = c

            # If both 1 and 9 are placed, check the sandwich sum
            if pos_1 is not None and pos_9 is not None:
                start = min(pos_1, pos_9) + 1
                end = max(pos_1, pos_9)

                sandwich_sum = 0
                all_filled = True
                for c in range(start, end):
                    val = grid[row][c] if (row, c) != (row, col) else num
                    if val == 0:
                        all_filled = False
                    else:
                        sandwich_sum += val

                # If all cells filled, must equal target
                if all_filled and sandwich_sum != target_sum:
                    return False
                # If partially filled, cannot exceed target
                elif sandwich_sum > target_sum:
                    return False

        # Check column constraint if this column has a sandwich clue
        if ('col', col) in self.sandwich_clues:
            target_sum = self.sandwich_clues[('col', col)]

            # Find positions of 1 and 9 in this column
            pos_1 = None
            pos_9 = None
            for r in range(self.size):
                val = grid[r][col] if (r, col) != (row, col) else num
                if val == 1:
                    pos_1 = r
                elif val == 9:
                    pos_9 = r

            # If both 1 and 9 are placed, check the sandwich sum
            if pos_1 is not None and pos_9 is not None:
                start = min(pos_1, pos_9) + 1
                end = max(pos_1, pos_9)

                sandwich_sum = 0
                all_filled = True
                for r in range(start, end):
                    val = grid[r][col] if (r, col) != (row, col) else num
                    if val == 0:
                        all_filled = False
                    else:
                        sandwich_sum += val

                # If all cells filled, must equal target
                if all_filled and sandwich_sum != target_sum:
                    return False
                # If partially filled, cannot exceed target
                elif sandwich_sum > target_sum:
                    return False

        return True


    def get_metadata(self):
        """Return metadata including sandwich clues."""
        metadata = super().get_metadata()
        metadata['sandwich_clues'] = {
            f"{direction}_{index}": sum_value
            for (direction, index), sum_value in self.sandwich_clues.items()
        }
        metadata['generation_mode'] = 'reverse' if len(self.sandwich_clues) > 3 else 'forward'
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return SandwichRule(size, box_size)
