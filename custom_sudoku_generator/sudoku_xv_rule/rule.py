import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class XVRule(BaseRule):
    """
    XV Sudoku: Cells separated by an X must sum to 10, cells separated by a V must sum to 5.
    Multiple X and V markers create interesting constraint patterns.

    This rule supports REVERSE GENERATION to ensure valid puzzles.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "XV Sudoku"
        self.description = "Specific adjacent cells must sum to 10 (X) or 5 (V)"

        # X and V pairs will be derived from solution or use defaults
        self.x_pairs = []
        self.v_pairs = []

    def supports_reverse_generation(self):
        """XV Sudoku benefits from reverse generation."""
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

    def _normalize_pair(self, pair):
        """
        Normalize a pair to ensure consistent ordering for overlap detection.
        Returns the pair as a frozenset of the two cell tuples.
        """
        return frozenset([pair[0], pair[1]])

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive X and V pairs from a completed Sudoku solution.

        Strategy:
        1. Find all adjacent pairs that sum to 10 (X) or 5 (V)
        2. Ensure no overlapping cells between pairs
        3. Select a reasonable number of each type for the puzzle
        """
        print("  Deriving XV constraints from solution...")

        self.x_pairs = []
        self.v_pairs = []

        # Track used cells to avoid overlapping
        used_cells = set()

        # Get all adjacent pairs
        all_pairs = self._get_adjacent_pairs()
        random.shuffle(all_pairs)

        # Find pairs that sum to 10 (X) - can have at most 8 per row/col
        potential_x_pairs = []
        for pair in all_pairs:
            (r1, c1), (r2, c2) = pair
            if solution_grid[r1][c1] + solution_grid[r2][c2] == 10:
                potential_x_pairs.append(pair)

        # Find pairs that sum to 5 (V) - can have 4 combinations: (1,4), (2,3), (3,2), (4,1)
        potential_v_pairs = []
        for pair in all_pairs:
            (r1, c1), (r2, c2) = pair
            if solution_grid[r1][c1] + solution_grid[r2][c2] == 5:
                potential_v_pairs.append(pair)

        random.shuffle(potential_x_pairs)
        random.shuffle(potential_v_pairs)

        # Select X pairs ensuring no overlap
        target_x_count = random.randint(6, 10)
        for pair in potential_x_pairs:
            if len(self.x_pairs) >= target_x_count:
                break
            (r1, c1), (r2, c2) = pair
            if (r1, c1) not in used_cells and (r2, c2) not in used_cells:
                self.x_pairs.append(pair)
                used_cells.add((r1, c1))
                used_cells.add((r2, c2))

        # Select V pairs ensuring no overlap (with X pairs or other V pairs)
        target_v_count = random.randint(5, 8)
        for pair in potential_v_pairs:
            if len(self.v_pairs) >= target_v_count:
                break
            (r1, c1), (r2, c2) = pair
            if (r1, c1) not in used_cells and (r2, c2) not in used_cells:
                self.v_pairs.append(pair)
                used_cells.add((r1, c1))
                used_cells.add((r2, c2))

        print(f"  Created {len(self.x_pairs)} X pairs and {len(self.v_pairs)} V pairs")

        return True

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the XV rule.
        """
        # Check X pairs (sum to 10)
        for cell1, cell2 in self.x_pairs:
            r1, c1 = cell1
            r2, c2 = cell2

            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0 and num + val2 != 10:
                    return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0 and val1 + num != 10:
                    return False

        # Check V pairs (sum to 5)
        for cell1, cell2 in self.v_pairs:
            r1, c1 = cell1
            r2, c2 = cell2

            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0 and num + val2 != 5:
                    return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0 and val1 + num != 5:
                    return False

        return True

    def get_metadata(self):
        """Return metadata including X and V pair markers."""
        metadata = super().get_metadata()
        metadata['x_pairs'] = [list(pair) for pair in self.x_pairs]
        metadata['v_pairs'] = [list(pair) for pair in self.v_pairs]
        metadata['generation_mode'] = 'reverse'
        return metadata

    def get_priority_removal_cells(self):
        """
        Return cells in XV pairs as priority for removal.
        This makes the puzzle more engaging by removing constraint cells first.
        """
        priority_cells = []
        for pair in self.x_pairs:
            priority_cells.extend(pair)
        for pair in self.v_pairs:
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
    return XVRule(size, box_size)
