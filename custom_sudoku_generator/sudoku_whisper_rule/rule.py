import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class WhisperRule(BaseRule):
    """
    Whisper Sudoku: Adjacent cells along whisper lines must differ by at least 5.
    Multiple whisper lines create interesting constraint patterns.

    This rule supports REVERSE GENERATION where whisper lines are created from
    a complete solution, finding paths where adjacent cells differ by at least 5.
    Lines are filtered to be longer than 5 cells and non-crossing.
    """

    # Constants for line generation
    MIN_LINE_LENGTH = 6  # Lines must be longer than 5 cells
    MAX_PATH_LENGTH = 15  # Maximum path length during exploration

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Whisper Sudoku"
        self.description = "Adjacent cells along whisper lines differ by at least 5"

        # Define whisper lines (lists of cells where adjacent pairs differ by at least 5)
        # Will be derived from solution or use defaults
        self.whisper_lines = []

    def supports_reverse_generation(self):
        """Whisper Sudoku strongly benefits from reverse generation."""
        return True

    def derive_constraints_from_solution(self, solution_grid):
        """
        Derive whisper lines from a completed Sudoku solution.

        Strategy:
        1. Find all paths where adjacent cells differ by at least 5
        2. Use both forward and reverse exploration to find longer lines
        3. Filter to keep only lines longer than 5 cells
        4. Ensure lines are not crossing (each cell belongs to only one line)
        """
        print("  Deriving whisper line constraints from solution...")

        self.whisper_lines = []
        used_cells = set()

        # Find all whisper lines using bidirectional path finding
        all_lines = self._find_all_whisper_lines(solution_grid)

        # Sort by length (prefer longer lines) and filter for minimum length
        all_lines = [line for line in all_lines if len(line) >= self.MIN_LINE_LENGTH]
        all_lines.sort(key=lambda x: len(x), reverse=True)

        # Select non-crossing lines
        for line in all_lines:
            # Check if any cell in this line is already used
            line_cells = set(line)
            if not line_cells.intersection(used_cells):
                self.whisper_lines.append(line)
                used_cells.update(line_cells)

        print(f"  Created {len(self.whisper_lines)} whisper lines (length >= {self.MIN_LINE_LENGTH}, non-crossing)")
        for i, line in enumerate(self.whisper_lines):
            print(f"    Line {i+1}: length {len(line)}")

        return len(self.whisper_lines) > 0

    def _find_all_whisper_lines(self, solution_grid):
        """
        Find all possible whisper lines in the solution.
        Uses a greedy exploration to find long whisper paths.
        """
        all_lines = []
        
        # Try starting from each cell and explore using greedy longest path
        for start_r in range(self.size):
            for start_c in range(self.size):
                # Find the longest path starting from this cell using greedy DFS
                line = self._find_longest_path_greedy((start_r, start_c), solution_grid)
                # Keep paths that might become valid after filtering (at least MIN_LINE_LENGTH - 2)
                if len(line) >= self.MIN_LINE_LENGTH - 2:
                    all_lines.append(line)

        return all_lines

    def _find_longest_path_greedy(self, start_cell, solution_grid):
        """
        Find a long whisper path from the given cell using greedy exploration.
        At each step, explores the direction that leads to the longest continuation.
        """
        best_path = [start_cell]
        
        # Try extending in all 8 directions and pick the best one
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # orthogonal
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonal
        ]
        
        for primary_dir in directions:
            # Try this as the primary direction
            path = self._build_path_in_direction(start_cell, primary_dir, solution_grid, set())
            
            # Also try extending backward (opposite direction)
            backward_dir = (-primary_dir[0], -primary_dir[1])
            backward_path = self._build_path_in_direction(start_cell, backward_dir, solution_grid, set(path))
            
            # Combine: reversed backward (without start) + forward path
            # backward_path[0] is start_cell, so skip it when reversing
            backward_without_start = list(reversed(backward_path[1:])) if len(backward_path) > 1 else []
            combined = backward_without_start + path
            
            if len(combined) > len(best_path):
                best_path = combined
        
        # Also try a more flexible snake-like path
        snake_path = self._build_snake_path(start_cell, solution_grid)
        if len(snake_path) > len(best_path):
            best_path = snake_path
        
        return best_path

    def _build_path_in_direction(self, start_cell, direction, solution_grid, excluded):
        """
        Build a path starting from start_cell, preferring the given direction.
        Falls back to any valid adjacent cell if the preferred direction is blocked.
        """
        path = [start_cell]
        visited = {start_cell} | excluded
        
        r, c = start_cell
        dr, dc = direction
        current_value = solution_grid[r][c]
        
        while len(path) < self.MAX_PATH_LENGTH:
            # Try preferred direction first
            preferred = (r + dr, c + dc)
            
            # Find all valid neighbors
            candidates = []
            for d in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nr, nc = r + d[0], c + d[1]
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if (nr, nc) not in visited:
                        next_value = solution_grid[nr][nc]
                        if abs(next_value - current_value) >= 5:
                            candidates.append((nr, nc, d))
            
            if not candidates:
                break
            
            # Prefer the primary direction if available, otherwise pick any valid one
            next_cell = None
            next_dir = None
            for nr, nc, d in candidates:
                if (nr, nc) == preferred:
                    next_cell = (nr, nc)
                    next_dir = d
                    break
            
            if next_cell is None:
                # Pick the first valid candidate
                next_cell = (candidates[0][0], candidates[0][1])
                next_dir = candidates[0][2]
            
            path.append(next_cell)
            visited.add(next_cell)
            r, c = next_cell
            dr, dc = next_dir
            current_value = solution_grid[r][c]
        
        return path

    def _build_snake_path(self, start_cell, solution_grid):
        """
        Build a snake-like path that can change direction.
        Uses greedy approach: always extend to the neighbor that has the most future options.
        """
        path = [start_cell]
        visited = {start_cell}
        
        r, c = start_cell
        current_value = solution_grid[r][c]
        
        while len(path) < self.MAX_PATH_LENGTH:
            # Find all valid neighbors
            candidates = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if (nr, nc) not in visited:
                        next_value = solution_grid[nr][nc]
                        if abs(next_value - current_value) >= 5:
                            # Count how many options this neighbor has
                            future_options = 0
                            for dr2, dc2 in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                                nnr, nnc = nr + dr2, nc + dc2
                                if 0 <= nnr < self.size and 0 <= nnc < self.size:
                                    if (nnr, nnc) not in visited and (nnr, nnc) != (r, c):
                                        nn_value = solution_grid[nnr][nnc]
                                        if abs(nn_value - next_value) >= 5:
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
        Check if placing 'num' at (row, col) violates the whisper rule.
        """
        # Check each whisper line
        for line in self.whisper_lines:
            if (row, col) in line:
                idx = line.index((row, col))

                # Check previous cell in line (must differ by at least 5)
                if idx > 0:
                    prev_r, prev_c = line[idx - 1]
                    prev_num = grid[prev_r][prev_c]
                    if prev_num != 0 and abs(num - prev_num) < 5:
                        return False

                # Check next cell in line (must differ by at least 5)
                if idx < len(line) - 1:
                    next_r, next_c = line[idx + 1]
                    next_num = grid[next_r][next_c]
                    if next_num != 0 and abs(num - next_num) < 5:
                        return False

        return True


    def get_metadata(self):
        """Return metadata including whisper lines."""
        metadata = super().get_metadata()
        metadata['whisper_lines'] = self.whisper_lines
        metadata['generation_mode'] = 'reverse' if len(self.whisper_lines) > 0 else 'forward'
        return metadata

    def get_priority_removal_cells(self):
        """
        Return cells in whisper lines as priority for removal.
        This makes the puzzle more engaging by removing constraint cells first.
        """
        priority_cells = []
        for line in self.whisper_lines:
            priority_cells.extend(line)
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
    return WhisperRule(size, box_size)
