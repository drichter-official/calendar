import sys
import os

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class ChainRule(BaseRule):
    """
    Chain Sudoku: Chain lines connect cells where adjacent cells in the chain
    must differ by exactly 1 (consecutive values).
    
    This rule supports REVERSE GENERATION where chain lines are created from
    a complete solution. The rule ensures:
    - At least 3 chain lines are generated
    - Chain lines do not overlap (no cell is used in more than one chain)
    - Lines are at least 3 cells long
    """

    # Constants for line generation
    MIN_LINE_LENGTH = 3
    MAX_LINE_LENGTH = 7
    MIN_LINES_REQUIRED = 3
    MAX_REGENERATION_ATTEMPTS = 10

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Chain Sudoku"
        self.description = "Chain lines connect cells with consecutive values"
        
        # Chain lines - lists of cells where adjacent cells differ by exactly 1
        self.chain_lines = []
        
        # Define corner cells of each 3x3 box (kept for backward compatibility)
        self.corner_cells = []
        for box_row in range(3):
            for box_col in range(3):
                top_left = (box_row * 3, box_col * 3)
                top_right = (box_row * 3, box_col * 3 + 2)
                bottom_left = (box_row * 3 + 2, box_col * 3)
                bottom_right = (box_row * 3 + 2, box_col * 3 + 2)
                self.corner_cells.extend([top_left, top_right, bottom_left, bottom_right])

    def supports_reverse_generation(self):
        """Chain Sudoku benefits from reverse generation."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive chain lines from a completed Sudoku solution.
        
        Strategy:
        1. Find all paths where adjacent cells differ by exactly 1 (consecutive)
        2. Ensure at least MIN_LINES_REQUIRED lines are found
        3. Ensure no overlapping cells between lines
        4. Return False to trigger regeneration if requirements not met
        """
        print("  Deriving chain line constraints from solution...")
        
        success = self._try_derive_chain_lines(solution_grid)
        
        if success:
            print(f"  Created {len(self.chain_lines)} chain lines (non-overlapping, min length {self.MIN_LINE_LENGTH})")
            for i, line in enumerate(self.chain_lines):
                print(f"    Line {i+1}: length {len(line)}")
            return True
        else:
            print(f"  Failed to find {self.MIN_LINES_REQUIRED} non-overlapping chain lines")
            return False

    def _try_derive_chain_lines(self, solution_grid):
        """
        Try to derive chain lines from the solution.
        Returns True if at least MIN_LINES_REQUIRED non-overlapping lines are found.
        """
        self.chain_lines = []
        used_cells = set()
        
        # Find all possible chain lines
        all_lines = self._find_all_chain_lines(solution_grid)
        
        # Filter valid lines and sort by length (prefer longer lines)
        valid_lines = [line for line in all_lines if self.MIN_LINE_LENGTH <= len(line) <= self.MAX_LINE_LENGTH]
        valid_lines.sort(key=lambda x: len(x), reverse=True)
        
        # Select non-overlapping lines
        for line in valid_lines:
            line_cells = set(line)
            if not line_cells.intersection(used_cells):
                self.chain_lines.append(line)
                used_cells.update(line_cells)
        
        # Check if we have at least MIN_LINES_REQUIRED lines
        return len(self.chain_lines) >= self.MIN_LINES_REQUIRED

    def _find_all_chain_lines(self, solution_grid):
        """
        Find all possible chain lines in the solution.
        A chain line consists of connected cells where adjacent cells differ by exactly 1.
        """
        all_lines = []
        
        # Find horizontal chain lines
        for r in range(self.size):
            c = 0
            while c < self.size:
                line = [(r, c)]
                while c + 1 < self.size and abs(solution_grid[r][c] - solution_grid[r][c+1]) == 1:
                    c += 1
                    line.append((r, c))
                if len(line) >= self.MIN_LINE_LENGTH:
                    all_lines.append(line)
                c += 1
        
        # Find vertical chain lines
        for c in range(self.size):
            r = 0
            while r < self.size:
                line = [(r, c)]
                while r + 1 < self.size and abs(solution_grid[r][c] - solution_grid[r+1][c]) == 1:
                    r += 1
                    line.append((r, c))
                if len(line) >= self.MIN_LINE_LENGTH:
                    all_lines.append(line)
                r += 1
        
        # Find diagonal chain lines (down-right)
        for start_r in range(self.size):
            for start_c in range(self.size):
                if start_r + self.MIN_LINE_LENGTH - 1 < self.size and start_c + self.MIN_LINE_LENGTH - 1 < self.size:
                    line = [(start_r, start_c)]
                    r, c = start_r, start_c
                    while r + 1 < self.size and c + 1 < self.size and abs(solution_grid[r][c] - solution_grid[r+1][c+1]) == 1:
                        r += 1
                        c += 1
                        line.append((r, c))
                    if len(line) >= self.MIN_LINE_LENGTH:
                        all_lines.append(line)
        
        # Find diagonal chain lines (down-left)
        for start_r in range(self.size):
            for start_c in range(self.size):
                if start_r + self.MIN_LINE_LENGTH - 1 < self.size and start_c - (self.MIN_LINE_LENGTH - 1) >= 0:
                    line = [(start_r, start_c)]
                    r, c = start_r, start_c
                    while r + 1 < self.size and c - 1 >= 0 and abs(solution_grid[r][c] - solution_grid[r+1][c-1]) == 1:
                        r += 1
                        c -= 1
                        line.append((r, c))
                    if len(line) >= self.MIN_LINE_LENGTH:
                        all_lines.append(line)
        
        # Also try to find snake-like paths using greedy exploration
        for start_r in range(self.size):
            for start_c in range(self.size):
                snake_line = self._find_snake_chain(solution_grid, (start_r, start_c))
                if len(snake_line) >= self.MIN_LINE_LENGTH:
                    # Avoid duplicates
                    if snake_line not in all_lines and list(reversed(snake_line)) not in all_lines:
                        all_lines.append(snake_line)
        
        return all_lines

    def _find_snake_chain(self, solution_grid, start_cell):
        """
        Find a chain line starting from start_cell using greedy exploration.
        The chain can turn (snake-like) to find longer paths.
        """
        path = [start_cell]
        visited = {start_cell}
        
        r, c = start_cell
        current_value = solution_grid[r][c]
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        while len(path) < self.MAX_LINE_LENGTH:
            candidates = []
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if (nr, nc) not in visited:
                        next_value = solution_grid[nr][nc]
                        if abs(next_value - current_value) == 1:
                            # Count future options for this candidate
                            future_options = 0
                            for dr2, dc2 in directions:
                                nnr, nnc = nr + dr2, nc + dc2
                                if 0 <= nnr < self.size and 0 <= nnc < self.size:
                                    if (nnr, nnc) not in visited and (nnr, nnc) != (r, c):
                                        nn_value = solution_grid[nnr][nnc]
                                        if abs(nn_value - next_value) == 1:
                                            future_options += 1
                            candidates.append((nr, nc, future_options))
            
            if not candidates:
                break
            
            # Sort by future options (descending) and pick the best
            candidates.sort(key=lambda x: x[2], reverse=True)
            next_cell = (candidates[0][0], candidates[0][1])
            
            path.append(next_cell)
            visited.add(next_cell)
            r, c = next_cell
            current_value = solution_grid[r][c]
        
        return path

    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the chain rule.
        Chain lines must have adjacent cells differing by exactly 1.
        """
        # Check each chain line
        for line in self.chain_lines:
            if (row, col) in line:
                idx = line.index((row, col))
                
                # Check previous cell in line (must differ by exactly 1)
                if idx > 0:
                    prev_r, prev_c = line[idx - 1]
                    prev_num = grid[prev_r][prev_c]
                    if prev_num != 0 and abs(num - prev_num) != 1:
                        return False
                
                # Check next cell in line (must differ by exactly 1)
                if idx < len(line) - 1:
                    next_r, next_c = line[idx + 1]
                    next_num = grid[next_r][next_c]
                    if next_num != 0 and abs(num - next_num) != 1:
                        return False
        
        # Also apply corner constraint for backward compatibility
        top_left_corners = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
        if (row, col) in top_left_corners:
            for r, c in top_left_corners:
                if (r, c) != (row, col) and grid[r][c] == num:
                    return False
        
        return True

    def get_metadata(self):
        """Return metadata including chain lines."""
        metadata = super().get_metadata()
        metadata['chain_lines'] = self.chain_lines
        metadata['corner_cells'] = self.corner_cells
        metadata['top_left_corners'] = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
        metadata['generation_mode'] = 'reverse' if len(self.chain_lines) >= self.MIN_LINES_REQUIRED else 'forward'
        return metadata

    def get_priority_removal_cells(self):
        """
        Return cells in chain lines as priority for removal.
        This makes the puzzle more engaging by removing constraint cells first.
        """
        priority_cells = []
        for line in self.chain_lines:
            priority_cells.extend(line)
        # Remove duplicates while preserving order (though lines shouldn't overlap)
        seen = set()
        unique_priority_cells = []
        for cell in priority_cells:
            if cell not in seen:
                seen.add(cell)
                unique_priority_cells.append(cell)
        return unique_priority_cells


# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return ChainRule(size, box_size)
