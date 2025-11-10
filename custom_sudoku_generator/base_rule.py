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

