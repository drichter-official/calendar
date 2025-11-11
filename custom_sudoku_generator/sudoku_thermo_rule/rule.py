import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ThermoRule(BaseRule):
    """
    Thermo Sudoku: Digits must strictly increase along thermometer lines.
    Multiple thermometers create interesting constraint patterns.

    This rule supports REVERSE GENERATION where thermometers are created from
    a complete solution, finding paths that naturally increase.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Thermo Sudoku"
        self.description = "Digits strictly increase along thermometer lines"

        # Define multiple thermometers as lists of cells
        self.thermometers = []

    def supports_reverse_generation(self):
        """Thermo Sudoku strongly benefits from reverse generation."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive thermometers from a completed Sudoku solution.

        Strategy:
        1. Find naturally increasing paths in the solution
        2. Create multiple thermometers of varying lengths (3-6 cells)
        3. Ensure good distribution across the grid
        """
        print("  Deriving thermometers from solution...")

        self.thermometers = []
        used_cells = set()

        # Try to create multiple thermometers
        num_thermos = random.randint(5, 10)
        attempts = 0
        max_attempts = 100

        while len(self.thermometers) < num_thermos and attempts < max_attempts:
            attempts += 1

            # Pick a random starting cell that's not used
            available_cells = [(r, c) for r in range(self.size) for c in range(self.size)
                             if (r, c) not in used_cells]

            if not available_cells:
                break

            start_cell = random.choice(available_cells)
            thermo = self._create_increasing_path(start_cell, solution_grid, used_cells, min_length=3, max_length=6)

            if len(thermo) >= 3:
                self.thermometers.append(thermo)
                for cell in thermo:
                    used_cells.add(cell)

        print(f"  Created {len(self.thermometers)} thermometers")

        return len(self.thermometers) > 0

    def _create_increasing_path(self, start_cell, solution_grid, used_cells, min_length=3, max_length=6):
        """
        Create a path of cells where values strictly increase.

        Args:
            start_cell: Starting (row, col) for the path
            solution_grid: The complete solution
            used_cells: Set of cells already used in other thermometers
            min_length: Minimum path length
            max_length: Maximum path length

        Returns:
            List of cells forming an increasing path
        """
        if start_cell in used_cells:
            return []

        r, c = start_cell
        path = [start_cell]
        current_value = solution_grid[r][c]

        # Try to extend the path
        while len(path) < max_length:
            r, c = path[-1]
            current_value = solution_grid[r][c]

            # Find adjacent cells with strictly higher values
            neighbors = [
                (r-1, c), (r+1, c), (r, c-1), (r, c+1)
            ]

            valid_neighbors = [
                (nr, nc) for nr, nc in neighbors
                if 0 <= nr < self.size and 0 <= nc < self.size
                and (nr, nc) not in used_cells
                and (nr, nc) not in path
                and solution_grid[nr][nc] > current_value
            ]

            if not valid_neighbors:
                break

            # Pick a random valid neighbor
            next_cell = random.choice(valid_neighbors)
            path.append(next_cell)

        # Only return path if it meets minimum length
        return path if len(path) >= min_length else []

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the thermo rule.
        """
        # Check each thermometer
        for thermo in self.thermometers:
            if (row, col) in thermo:
                idx = thermo.index((row, col))

                # Check previous cell (should be less)
                if idx > 0:
                    prev_r, prev_c = thermo[idx - 1]
                    prev_num = grid[prev_r][prev_c]
                    if prev_num != 0 and prev_num >= num:
                        return False

                # Check next cell (should be greater)
                if idx < len(thermo) - 1:
                    next_r, next_c = thermo[idx + 1]
                    next_num = grid[next_r][next_c]
                    if next_num != 0 and next_num <= num:
                        return False

        return True


    def get_metadata(self):
        """Return metadata including thermometer information."""
        metadata = super().get_metadata()
        metadata['thermometers'] = self.thermometers
        metadata['generation_mode'] = 'reverse' if len(self.thermometers) > 3 else 'forward'
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ThermoRule(size, box_size)
