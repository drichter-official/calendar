import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ConsecutiveRule(BaseRule):
    """
    Consecutive Sudoku: White dots mark where orthogonally adjacent cells contain consecutive numbers.
    If no dot is marked between cells, they CANNOT be consecutive.

    This rule supports REVERSE GENERATION to ensure valid puzzles.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Consecutive Sudoku"
        self.description = "Marked cells must be consecutive, unmarked cells cannot be"

        # Define pairs where consecutive is ALLOWED (white dots)
        # Will be derived from solution or use defaults
        self.consecutive_pairs = set()

    def supports_reverse_generation(self):
        """Consecutive Sudoku strongly benefits from reverse generation."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive consecutive markers from a completed Sudoku solution.

        Strategy:
        1. Find all adjacent pairs that ARE consecutive in the solution
        2. Mark a subset of them (not all - that would be too easy)
        3. Ensure the remaining non-marked pairs are NOT consecutive
        """
        print("  Deriving consecutive constraints from solution...")

        self.consecutive_pairs = set()

        # Find all pairs that are consecutive in the solution
        consecutive_in_solution = []
        non_consecutive_in_solution = []

        for r in range(self.size):
            for c in range(self.size):
                # Check right neighbor
                if c < self.size - 1:
                    if abs(solution_grid[r][c] - solution_grid[r][c+1]) == 1:
                        consecutive_in_solution.append(((r, c), (r, c+1)))
                    else:
                        non_consecutive_in_solution.append(((r, c), (r, c+1)))

                # Check down neighbor
                if r < self.size - 1:
                    if abs(solution_grid[r][c] - solution_grid[r+1][c]) == 1:
                        consecutive_in_solution.append(((r, c), (r+1, c)))
                    else:
                        non_consecutive_in_solution.append(((r, c), (r+1, c)))

        # Mark a random subset of consecutive pairs (30-50%)
        if consecutive_in_solution:
            num_to_mark = random.randint(len(consecutive_in_solution) // 3, len(consecutive_in_solution) // 2)
            self.consecutive_pairs = set(random.sample(consecutive_in_solution, num_to_mark))

        print(f"  Created {len(self.consecutive_pairs)} consecutive markers")
        print(f"  ({len(consecutive_in_solution)} consecutive pairs in solution)")

        return True

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the consecutive rule.
        """
        # Check all orthogonally adjacent cells
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                adjacent_num = grid[nr][nc]
                if adjacent_num != 0:
                    is_consecutive = abs(adjacent_num - num) == 1

                    # Check if this pair is marked as consecutive
                    pair1 = ((row, col), (nr, nc))
                    pair2 = ((nr, nc), (row, col))
                    is_marked = pair1 in self.consecutive_pairs or pair2 in self.consecutive_pairs

                    # If consecutive but not marked, invalid
                    if is_consecutive and not is_marked:
                        return False

        return True


    def get_metadata(self):
        """Return metadata including consecutive pair markers."""
        metadata = super().get_metadata()
        metadata['consecutive_pairs'] = [list(pair) for pair in self.consecutive_pairs]
        metadata['generation_mode'] = 'reverse' if len(self.consecutive_pairs) > 5 else 'forward'
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ConsecutiveRule(size, box_size)
