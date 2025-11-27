import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class KropkiRule(BaseRule):
    """
    Kropki Sudoku: White dots between cells mean they differ by 1,
    black dots mean one is double the other.

    This rule supports REVERSE GENERATION to ensure valid puzzles.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Kropki Sudoku"
        self.description = "White dots: cells differ by 1. Black dots: one cell is double the other"

        # White and black dots will be derived from solution or use defaults
        self.white_dots = []
        self.black_dots = []

    def supports_reverse_generation(self):
        """Kropki Sudoku benefits from reverse generation."""
        return True

    def _get_adjacent_pairs(self):
        """
        Get all possible adjacent cell pairs (horizontal and vertical).
        Returns list of ((r1, c1), (r2, c2)) tuples.
        """
        pairs = []
        for r in range(self.size):
            for c in range(self.size):
                # Horizontal pair
                if c + 1 < self.size:
                    pairs.append(((r, c), (r, c + 1)))
                # Vertical pair
                if r + 1 < self.size:
                    pairs.append(((r, c), (r + 1, c)))
        return pairs

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive white and black dots from a completed Sudoku solution.

        Strategy:
        1. Find all adjacent pairs that differ by 1 (white dots) or have 1:2 ratio (black dots)
        2. Select a reasonable number of each type for the puzzle
        """
        print("  Deriving Kropki constraints from solution...")

        self.white_dots = []
        self.black_dots = []

        # Get all adjacent pairs
        all_pairs = self._get_adjacent_pairs()

        # Find pairs that differ by 1 (white dots)
        potential_white = []
        for pair in all_pairs:
            (r1, c1), (r2, c2) = pair
            if abs(solution_grid[r1][c1] - solution_grid[r2][c2]) == 1:
                potential_white.append(pair)

        # Find pairs with 1:2 ratio (black dots)
        potential_black = []
        for pair in all_pairs:
            (r1, c1), (r2, c2) = pair
            v1 = solution_grid[r1][c1]
            v2 = solution_grid[r2][c2]
            if v1 * 2 == v2 or v2 * 2 == v1:
                potential_black.append(pair)

        random.shuffle(potential_white)
        random.shuffle(potential_black)

        # Select white dots (consecutive pairs)
        target_white_count = random.randint(8, 14)
        self.white_dots = potential_white[:min(target_white_count, len(potential_white))]

        # Select black dots (ratio pairs)
        target_black_count = random.randint(6, 10)
        self.black_dots = potential_black[:min(target_black_count, len(potential_black))]

        print(f"  Created {len(self.white_dots)} white dots and {len(self.black_dots)} black dots")

        return True

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the kropki rule.
        """
        # Check white dots (differ by 1)
        for cell1, cell2 in self.white_dots:
            r1, c1 = cell1
            r2, c2 = cell2

            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0 and abs(num - val2) != 1:
                    return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0 and abs(val1 - num) != 1:
                    return False

        # Check black dots (ratio 1:2)
        for cell1, cell2 in self.black_dots:
            r1, c1 = cell1
            r2, c2 = cell2

            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0 and not (num * 2 == val2 or val2 * 2 == num):
                    return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0 and not (val1 * 2 == num or num * 2 == val1):
                    return False

        return True

    def get_metadata(self):
        """Return metadata including white and black dot markers."""
        metadata = super().get_metadata()
        # Convert tuples to lists for JSON serialization
        metadata['white_dots'] = [
            [list(cell) for cell in pair] for pair in self.white_dots
        ]
        metadata['black_dots'] = [
            [list(cell) for cell in pair] for pair in self.black_dots
        ]
        metadata['generation_mode'] = 'reverse'
        return metadata

    def get_priority_removal_cells(self):
        """
        Return cells in Kropki dots as priority for removal.
        This makes the puzzle more engaging by removing constraint cells first.
        """
        priority_cells = []
        for pair in self.white_dots:
            priority_cells.extend(pair)
        for pair in self.black_dots:
            priority_cells.extend(pair)
        # Remove duplicates while preserving order
        seen = set()
        unique_priority_cells = []
        for cell in priority_cells:
            if cell not in seen:
                seen.add(cell)
                unique_priority_cells.append(cell)
        return unique_priority_cells


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return KropkiRule(size, box_size)
