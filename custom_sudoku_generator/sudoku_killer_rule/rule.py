import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class KillerRule(BaseRule):
    """
    Killer Sudoku: Groups of cells (cages) must sum to specific values, and no digit
    can repeat within a cage. Cages are defined with target sums.

    This rule supports REVERSE GENERATION where cages are derived from a complete
    solution, making generation much faster and guaranteed to produce valid puzzles.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Killer Sudoku"
        self.description = "Cages must sum to specific values with no repeated digits"
        
        # Cages will be derived from solution or predefined
        # Format: [(target_sum, [cells]), ...]
        self.cages = []
        self.cell_to_cage = {}

    def supports_reverse_generation(self):
        """Killer Sudoku strongly benefits from reverse generation."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive killer cages from a completed Sudoku solution.

        Strategy:
        1. Create random cage shapes (2-5 cells each)
        2. Ensure no cage crosses box boundaries (optional, makes it easier)
        3. Calculate the sum for each cage from the solution
        4. Ensure good coverage of the grid
        """
        print("  Deriving killer cages from solution...")

        self.cages = []
        self.cell_to_cage = {}

        # Track which cells are already in cages
        used_cells = set()

        # Try to create cages for all cells
        attempts = 0
        max_attempts = 1000

        while len(used_cells) < self.size * self.size and attempts < max_attempts:
            attempts += 1

            # Pick a random unclaimed cell
            available_cells = [(r, c) for r in range(self.size) for c in range(self.size)
                             if (r, c) not in used_cells]

            if not available_cells:
                break

            start_cell = random.choice(available_cells)
            cage_cells = self._create_random_cage(start_cell, used_cells, min_size=2, max_size=5)

            if len(cage_cells) > 0:
                # Calculate the target sum from the solution
                target_sum = sum(solution_grid[r][c] for r, c in cage_cells)

                # Add this cage
                cage_idx = len(self.cages)
                self.cages.append((target_sum, cage_cells))

                for cell in cage_cells:
                    used_cells.add(cell)
                    self.cell_to_cage[cell] = cage_idx

        print(f"  Created {len(self.cages)} killer cages covering {len(used_cells)}/{self.size * self.size} cells")

        return len(self.cages) > 0

    def _create_random_cage(self, start_cell, used_cells, min_size=2, max_size=5):
        """
        Create a random contiguous cage starting from start_cell.

        Args:
            start_cell: Starting (row, col) for the cage
            used_cells: Set of cells already used in other cages
            min_size: Minimum cage size
            max_size: Maximum cage size

        Returns:
            List of cells in the cage
        """
        if start_cell in used_cells:
            return []

        cage = [start_cell]
        candidates = [start_cell]
        target_size = random.randint(min_size, max_size)

        while len(cage) < target_size and candidates:
            # Pick a random cell from current cage to expand from
            current = random.choice(candidates)
            r, c = current

            # Find adjacent cells (up, down, left, right)
            neighbors = [
                (r-1, c), (r+1, c), (r, c-1), (r, c+1)
            ]

            # Filter valid neighbors
            valid_neighbors = [
                (nr, nc) for nr, nc in neighbors
                if 0 <= nr < self.size and 0 <= nc < self.size
                and (nr, nc) not in used_cells
                and (nr, nc) not in cage
            ]

            if valid_neighbors:
                # Add a random valid neighbor
                new_cell = random.choice(valid_neighbors)
                cage.append(new_cell)
                candidates.append(new_cell)
            else:
                # This cell has no more valid neighbors
                candidates.remove(current)

        # Only return cage if it meets minimum size
        if len(cage) >= min_size:
            return cage
        else:
            return [start_cell] if start_cell not in used_cells else []

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the killer rule.
        Optimized for performance during puzzle solving.
        """
        # Find which cage this cell belongs to (fast lookup via dict)
        if (row, col) not in self.cell_to_cage:
            return True  # Cell not in any cage, no constraint

        cage_idx = self.cell_to_cage[(row, col)]
        target_sum, cage_cells = self.cages[cage_idx]

        # Check for duplicate in the same cage (early exit on duplicate)
        for r, c in cage_cells:
            if (r, c) != (row, col) and grid[r][c] == num:
                return False

        # Check sum constraint
        current_sum = num
        filled_count = 1

        for r, c in cage_cells:
            if (r, c) != (row, col):
                val = grid[r][c]
                if val != 0:
                    current_sum += val
                    filled_count += 1
                    # Early exit: if we already exceed target, fail immediately
                    if current_sum > target_sum:
                        return False

        # If all cells filled, must match target exactly
        if filled_count == len(cage_cells):
            return current_sum == target_sum

        # Partially filled: we already checked we don't exceed, so OK
        return True

    def get_metadata(self):
        """Return metadata including cage information."""
        metadata = super().get_metadata()
        metadata['cages'] = [
            {
                'sum': target_sum,
                'cells': cells
            }
            for target_sum, cells in self.cages
        ]
        metadata['generation_mode'] = 'reverse' if len(self.cages) > 10 else 'forward'
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return KillerRule(size, box_size)
