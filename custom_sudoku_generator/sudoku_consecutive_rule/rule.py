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
    Consecutive Sudoku: Marked lines contain consecutive numbers in sequence.
    Each line is shown in a different color.

    This rule supports REVERSE GENERATION to ensure valid puzzles.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Consecutive Sudoku"
        self.description = "Marked lines must contain consecutive numbers in sequence"

        # Define consecutive lines (lists of cells that must contain consecutive numbers)
        # Will be derived from solution or use defaults
        self.consecutive_lines = []

    def supports_reverse_generation(self):
        """Consecutive Sudoku strongly benefits from reverse generation."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive consecutive lines from a completed Sudoku solution.

        Strategy:
        1. Find all consecutive sequences in the solution (horizontal, vertical, and diagonal)
        2. Prefer longer lines (length 3 or more)
        3. Ensure good variety and coverage
        """
        print("  Deriving consecutive line constraints from solution...")

        self.consecutive_lines = []

        # Find all consecutive sequences (horizontal)
        for r in range(self.size):
            c = 0
            while c < self.size:
                line = [(r, c)]
                while c + 1 < self.size and abs(solution_grid[r][c] - solution_grid[r][c+1]) == 1:
                    c += 1
                    line.append((r, c))

                if len(line) >= 3:  # Keep lines of length 3 or more
                    self.consecutive_lines.append(line)

                c += 1

        # Find all consecutive sequences (vertical)
        for c in range(self.size):
            r = 0
            while r < self.size:
                line = [(r, c)]
                while r + 1 < self.size and abs(solution_grid[r][c] - solution_grid[r+1][c]) == 1:
                    r += 1
                    line.append((r, c))

                if len(line) >= 3:  # Keep lines of length 3 or more
                    self.consecutive_lines.append(line)

                r += 1

        # Find diagonal consecutive sequences (down-right)
        for start_r in range(self.size):
            for start_c in range(self.size):
                if start_r + 2 < self.size and start_c + 2 < self.size:  # At least 3 cells
                    line = [(start_r, start_c)]
                    r, c = start_r, start_c
                    while r + 1 < self.size and c + 1 < self.size and abs(solution_grid[r][c] - solution_grid[r+1][c+1]) == 1:
                        r += 1
                        c += 1
                        line.append((r, c))

                    if len(line) >= 3:
                        self.consecutive_lines.append(line)

        # Find diagonal consecutive sequences (down-left)
        for start_r in range(self.size):
            for start_c in range(self.size):
                if start_r + 2 < self.size and start_c - 2 >= 0:  # At least 3 cells
                    line = [(start_r, start_c)]
                    r, c = start_r, start_c
                    while r + 1 < self.size and c - 1 >= 0 and abs(solution_grid[r][c] - solution_grid[r+1][c-1]) == 1:
                        r += 1
                        c -= 1
                        line.append((r, c))

                    if len(line) >= 3:
                        self.consecutive_lines.append(line)

        # Sort by length (prefer longer lines) and randomly select subset
        if len(self.consecutive_lines) > 0:
            # Sort by length descending
            self.consecutive_lines.sort(key=lambda x: len(x), reverse=True)

            # Keep the best ones (40-60% of found lines, minimum 3, maximum 8)
            num_to_keep = max(3, min(8, len(self.consecutive_lines) * random.randint(40, 60) // 100))

            # Bias towards longer lines by keeping more from the top
            if len(self.consecutive_lines) > num_to_keep:
                # Keep 80% from top half (longer lines) and 20% from bottom half (shorter lines)
                top_count = int(num_to_keep * 0.8)
                bottom_count = num_to_keep - top_count

                mid_point = len(self.consecutive_lines) // 2
                selected = random.sample(self.consecutive_lines[:mid_point], min(top_count, mid_point))
                if bottom_count > 0 and len(self.consecutive_lines) > mid_point:
                    selected += random.sample(self.consecutive_lines[mid_point:], min(bottom_count, len(self.consecutive_lines) - mid_point))

                self.consecutive_lines = selected

        print(f"  Created {len(self.consecutive_lines)} consecutive lines")
        for i, line in enumerate(self.consecutive_lines):
            print(f"    Line {i+1}: length {len(line)}")

        return True

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the consecutive rule.
        A line must contain consecutive numbers in sequence (in any order).
        """
        # Check each consecutive line
        for line in self.consecutive_lines:
            if (row, col) in line:
                # Get all filled values in this line (including current)
                values = []
                for r, c in line:
                    if (r, c) == (row, col):
                        values.append(num)
                    elif grid[r][c] != 0:
                        values.append(grid[r][c])

                # If more than one value, check if they form a consecutive sequence
                if len(values) > 1:
                    sorted_vals = sorted(values)
                    for i in range(len(sorted_vals) - 1):
                        if sorted_vals[i + 1] - sorted_vals[i] != 1:
                            return False

                    # Also check if we can fit remaining values
                    # The range must be able to fit in the line length
                    if len(values) == len(line):
                        expected_range = sorted_vals[-1] - sorted_vals[0] + 1
                        if expected_range != len(line):
                            return False

        return True


    def get_metadata(self):
        """Return metadata including consecutive lines."""
        metadata = super().get_metadata()
        metadata['consecutive_lines'] = self.consecutive_lines
        metadata['generation_mode'] = 'reverse' if len(self.consecutive_lines) > 3 else 'forward'
        return metadata

    def get_priority_removal_cells(self):
        """
        Return cells in consecutive lines as priority for removal.
        This makes the puzzle more engaging by removing constraint cells first.
        """
        priority_cells = []
        for line in self.consecutive_lines:
            priority_cells.extend(line)
        # Remove duplicates (in case lines overlap) while preserving order
        seen = set()
        unique_priority_cells = []
        for cell in priority_cells:
            if cell not in seen:
                seen.add(cell)
                unique_priority_cells.append(cell)
        return unique_priority_cells


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ConsecutiveRule(size, box_size)
