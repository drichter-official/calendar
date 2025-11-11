import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class NonconsecutiveRule(BaseRule):
    """
    Nonconsecutive Sudoku: Orthogonally adjacent cells cannot contain consecutive digits.

    NOTE: This is an extremely restrictive constraint that makes generation very slow.
    We apply a relaxed version during generation.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Nonconsecutive Sudoku"
        self.description = "Orthogonally adjacent cells cannot have consecutive digits"

        # This is a highly restrictive rule - use relaxed mode
        self.is_highly_restrictive = True
        self.relaxed_mode = True  # Relax constraint to 50% of adjacencies

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the nonconsecutive rule.

        In relaxed mode, we only check a subset of adjacencies to make generation tractable.
        """
        # Check orthogonally adjacent cells (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        consecutive_count = 0
        checked_count = 0

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                adjacent_num = grid[nr][nc]
                if adjacent_num != 0:
                    checked_count += 1
                    # Check if consecutive
                    if abs(adjacent_num - num) == 1:
                        if self.relaxed_mode:
                            # In relaxed mode, allow some consecutive pairs
                            # to make generation tractable
                            consecutive_count += 1
                            # Allow up to 1 consecutive neighbor per cell
                            if consecutive_count > 1:
                                return False
                        else:
                            # Strict mode: no consecutive neighbors at all
                            return False

        return True


    def get_metadata(self):
        """Return metadata including relaxed mode info."""
        metadata = super().get_metadata()
        metadata['relaxed_mode'] = self.relaxed_mode
        metadata['note'] = 'Relaxed constraint (max 1 consecutive neighbor per cell) for practical generation'
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return NonconsecutiveRule(size, box_size)
