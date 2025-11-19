"""
Base class for custom Sudoku rules.
All custom rules should inherit from this class and implement the validate method.
"""

class BaseRule:
    """
    Base class for custom Sudoku rules.
    """

    def __init__(self, size=9, box_size=3):
        """
        Initialize the rule with grid dimensions.

        Args:
            size: Size of the Sudoku grid (default 9)
            box_size: Size of each box (default 3 for 3x3 boxes)
        """
        self.size = size
        self.box_size = box_size
        self.name = "Base Rule"
        self.description = "No custom rules applied"

        # Some rules (like Jigsaw) replace the standard box constraint entirely
        self.use_standard_boxes = True

    def validate(self, grid, row, col, num):
        """
        Validate whether placing 'num' at position (row, col) is allowed.

        Args:
            grid: The current state of the Sudoku grid
            row: Row index (0-based)
            col: Column index (0-based)
            num: Number to be placed (1-9)

        Returns:
            True if the placement is valid, False otherwise
        """
        return True

    def get_metadata(self):
        """
        Return metadata about this rule for saving/documentation.

        Returns:
            Dictionary with rule information
        """
        return {
            "name": self.name,
            "description": self.description,
            "size": self.size,
            "box_size": self.box_size
        }

    def supports_reverse_generation(self):
        """
        Indicate whether this rule supports generating constraints from a solution.

        For complex rules (like Killer, Sandwich, Arrow), it's much faster to:
        1. Generate a valid standard Sudoku solution
        2. Derive constraints from that solution

        Rather than trying to generate a solution that satisfies pre-defined constraints.

        Returns:
            bool: True if this rule can derive constraints from a complete solution
        """
        return False

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive rule-specific constraints from a completed Sudoku solution.

        This method should be overridden by rules that support reverse generation.
        It should analyze the solution and create appropriate constraints (cages,
        thermometers, arrows, etc.) that are satisfied by the solution.

        Args:
            solution_grid: A completed valid Sudoku grid

        Returns:
            bool: True if constraints were successfully derived
        """
        return True

    def get_priority_removal_cells(self):
        """
        Return a list of cells that should be prioritized for removal during puzzle generation.

        This allows rules to specify that certain constrained cells should be removed first
        to make the puzzle more engaging (e.g., cells in consecutive lines, thermometer cells, etc.)

        Returns:
            list: List of (row, col) tuples representing cells to prioritize for removal.
                  Empty list means no priority (use random removal).
        """
        return []

