import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class FutoshikiRule(BaseRule):
    """
    Futoshiki Sudoku: Inequality signs between cells indicate greater/less than relationships.
    Multiple inequalities create interesting constraint patterns.

    This rule supports REVERSE GENERATION to ensure valid puzzles.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Futoshiki Sudoku"
        self.description = "Inequality constraints between adjacent cells"

        # Inequalities will be derived from solution or use defaults
        # Format: [(cell1, cell2, operator), ...]
        # operator: '<' means cell1 < cell2, '>' means cell1 > cell2
        self.inequalities = []

    def supports_reverse_generation(self):
        """Futoshiki Sudoku benefits from reverse generation."""
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
        Derive inequality constraints from a completed Sudoku solution.

        Strategy:
        1. Find all adjacent pairs that have a < or > relationship
        2. Ensure no overlapping cells between pairs
        3. Select a reasonable number of inequalities for the puzzle
        """
        print("  Deriving Futoshiki constraints from solution...")

        self.inequalities = []

        # Track used cells to avoid overlapping
        used_cells = set()

        # Get all adjacent pairs
        all_pairs = self._get_adjacent_pairs()
        random.shuffle(all_pairs)

        # For each pair, determine the inequality relationship
        potential_inequalities = []
        for pair in all_pairs:
            (r1, c1), (r2, c2) = pair
            val1 = solution_grid[r1][c1]
            val2 = solution_grid[r2][c2]
            if val1 < val2:
                potential_inequalities.append((pair[0], pair[1], '<'))
            elif val1 > val2:
                potential_inequalities.append((pair[0], pair[1], '>'))

        random.shuffle(potential_inequalities)

        # Select inequalities ensuring no overlap
        target_count = random.randint(12, 18)
        for cell1, cell2, operator in potential_inequalities:
            if len(self.inequalities) >= target_count:
                break
            if cell1 not in used_cells and cell2 not in used_cells:
                self.inequalities.append((cell1, cell2, operator))
                used_cells.add(cell1)
                used_cells.add(cell2)

        print(f"  Created {len(self.inequalities)} inequality constraints")

        return True

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the futoshiki rule.
        """
        for cell1, cell2, operator in self.inequalities:
            r1, c1 = cell1
            r2, c2 = cell2

            # Check if current placement is involved in this inequality
            if (row, col) == (r1, c1):
                val2 = grid[r2][c2]
                if val2 != 0:
                    if operator == '<' and num >= val2:
                        return False
                    elif operator == '>' and num <= val2:
                        return False
            elif (row, col) == (r2, c2):
                val1 = grid[r1][c1]
                if val1 != 0:
                    if operator == '<' and val1 >= num:
                        return False
                    elif operator == '>' and val1 <= num:
                        return False

        return True

    def get_metadata(self):
        """Return metadata including inequality constraints."""
        metadata = super().get_metadata()
        metadata['inequalities'] = [
            {
                'cell1': list(cell1),
                'cell2': list(cell2),
                'operator': operator
            }
            for cell1, cell2, operator in self.inequalities
        ]
        metadata['generation_mode'] = 'reverse'
        return metadata

    def get_priority_removal_cells(self):
        """
        Return cells in inequalities as priority for removal.
        This makes the puzzle more engaging by removing constraint cells first.
        """
        priority_cells = []
        for cell1, cell2, _ in self.inequalities:
            priority_cells.append(cell1)
            priority_cells.append(cell2)
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
    return FutoshikiRule(size, box_size)
