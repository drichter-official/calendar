import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class FutoshikiRule(BaseRule):
    """
    Futoshiki Sudoku: Inequality signs between cells indicate greater/less than relationships.
    Multiple inequalities create interesting constraint patterns.
    """

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Futoshiki Sudoku"
        self.description = "Inequality constraints between adjacent cells"

        # Define inequalities: (cell1, cell2, operator)
        # operator: '<' means cell1 < cell2, '>' means cell1 > cell2
        self.inequalities = [
            ((0, 0), (0, 1), '<'),  # (0,0) < (0,1)
            ((0, 1), (0, 2), '<'),  # (0,1) < (0,2)
            ((0, 3), (0, 4), '>'),  # (0,3) > (0,4)
            ((1, 0), (2, 0), '<'),  # (1,0) < (2,0)
            ((2, 2), (2, 3), '>'),  # (2,2) > (2,3)
            ((3, 0), (4, 0), '>'),  # (3,0) > (4,0)
            ((4, 4), (5, 4), '<'),  # (4,4) < (5,4)
            ((5, 5), (5, 6), '<'),  # (5,5) < (5,6)
            ((6, 6), (7, 6), '>'),  # (6,6) > (7,6)
            ((8, 7), (8, 8), '<'),  # (8,7) < (8,8)
        ]

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


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return FutoshikiRule(size, box_size)
