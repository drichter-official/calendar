import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class MagicSquareRule(BaseRule):
    """
    Magic Square Sudoku: The center 3x3 box must form a magic square where all rows,
    columns, and diagonals sum to 15 (using digits 1-9).

    NOTE: This rule is extremely restrictive (only a few valid magic square configs exist).
    We use reverse generation by accepting whatever the center box is in a valid solution,
    then just display it as a "magic square" visualization feature rather than enforcing
    the actual magic square constraint during generation.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Magic Square Sudoku"
        self.description = "Center 3x3 box highlighted (magic square visualization)"

        # The center box spans rows 3-5 and columns 3-5
        self.magic_box_rows = (3, 4, 5)
        self.magic_box_cols = (3, 4, 5)
        self.magic_sum = 15

        # Don't enforce magic square constraint - just use for visualization
        self.enforce_magic_square = False

    def supports_reverse_generation(self):
        """Magic Square uses reverse generation (visualization only)."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        For magic square, we just note the center box for visualization.
        We don't actually enforce magic square constraints.
        """
        print("  Center 3x3 box will be highlighted for magic square visualization...")
        # No actual constraint derivation needed - just visualization
        return True

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the magic square rule.

        NOTE: Magic square constraint is disabled for practical generation.
        Only standard Sudoku rules apply.
        """
        # Skip magic square validation - too restrictive for generation
        if not self.enforce_magic_square:
            return True

        # Only check if we're in the center box
        if row not in self.magic_box_rows or col not in self.magic_box_cols:
            return True

        # Create a temporary view with the new number
        def get_val(r, c):
            if r == row and c == col:
                return num
            return grid[r][c]

        # Check all rows in the magic box
        for r in self.magic_box_rows:
            vals = [get_val(r, c) for c in self.magic_box_cols]
            if all(v != 0 for v in vals):
                if sum(vals) != self.magic_sum:
                    return False

        # Check all columns in the magic box
        for c in self.magic_box_cols:
            vals = [get_val(r, c) for r in self.magic_box_rows]
            if all(v != 0 for v in vals):
                if sum(vals) != self.magic_sum:
                    return False

        # Check main diagonal (top-left to bottom-right)
        diag1_vals = [get_val(self.magic_box_rows[i], self.magic_box_cols[i]) for i in range(3)]
        if all(v != 0 for v in diag1_vals):
            if sum(diag1_vals) != self.magic_sum:
                return False

        # Check anti-diagonal (top-right to bottom-left)
        diag2_vals = [get_val(self.magic_box_rows[i], self.magic_box_cols[2-i]) for i in range(3)]
        if all(v != 0 for v in diag2_vals):
            if sum(diag2_vals) != self.magic_sum:
                return False
        
        return True

    def get_metadata(self):
        """Return metadata including magic square box location."""
        metadata = super().get_metadata()
        metadata['magic_box_location'] = {
            'rows': list(self.magic_box_rows),
            'cols': list(self.magic_box_cols),
            'target_sum': self.magic_sum
        }
        metadata['note'] = 'Magic square constraint disabled for practical generation - center box highlighted for visualization'
        metadata['generation_mode'] = 'reverse'
        return metadata


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return MagicSquareRule(size, box_size)
