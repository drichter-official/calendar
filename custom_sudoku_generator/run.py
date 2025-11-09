import random
import copy

class SudokuGenerator:
    def __init__(self, size=9, box_size=3):
        self.size = size              # 9 for classic Sudoku
        self.box_size = box_size      # 3 for classic Sudoku (3x3 boxes)
        self.grid = [[0]*size for _ in range(size)]

    def is_valid(self, grid, row, col, num):
        # Standard Sudoku rules
        box_row_start = (row // self.box_size) * self.box_size
        box_col_start = (col // self.box_size) * self.box_size

        if any(grid[row][i] == num for i in range(self.size)):
            return False
        if any(grid[i][col] == num for i in range(self.size)):
            return False
        for r in range(box_row_start, box_row_start + self.box_size):
            for c in range(box_col_start, box_col_start + self.box_size):
                if grid[r][c] == num:
                    return False

        # Custom rule checks (add your rules here)
        # Example: shapes must satisfy some condition:
        if not self.custom_rule(grid, row, col, num):
            return False

        return True

    def custom_rule(self, grid, row, col, num):
        box_row_start = (row // self.box_size) * self.box_size
        box_col_start = (col // self.box_size) * self.box_size

        # Create a temporary grid to test the placement
        temp_grid = [list(r) for r in grid]
        temp_grid[row][col] = num

        # Get the diagonal elements of the 3x3 box
        diag1 = []
        diag2 = []
        for i in range(self.box_size):
            diag1.append(temp_grid[box_row_start + i][box_col_start + i])
            diag2.append(temp_grid[box_row_start + i][box_col_start + (self.box_size - 1 - i)])

        def sum_check(diag):
            # If there's an empty cell (0), allow partial checks (sum ≤ 13)
            if 0 in diag:
                return sum(x for x in diag if x != 0) <= 13
            # If fully filled, sum must exactly be 13
            return sum(diag) == 13

        if not sum_check(diag1):
            return False
        if not sum_check(diag2):
            return False

        return True



        # You can keep other custom rules here or add more conditions.

        return True

    def solve(self, grid):
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self.solve(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    def generate_full_grid(self):
        self.grid = [[0]*self.size for _ in range(self.size)]
        self._fill_grid(self.grid)
        return self.grid

    def _fill_grid(self, grid):
        empty = self._find_empty(grid)
        if not empty:
            return True
        row, col = empty

        nums = list(range(1, self.size+1))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(grid, row, col, num):
                grid[row][col] = num
                if self._fill_grid(grid):
                    return True
                grid[row][col] = 0
        return False

    def _find_empty(self, grid):
        for r in range(self.size):
            for c in range(self.size):
                if grid[r][c] == 0:
                    return r, c
        return None

    # Remove clues while ensuring unique solution
    def remove_numbers(self, attempts=5):
        grid = copy.deepcopy(self.grid)
        while attempts > 0:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            while grid[row][col] == 0:
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
            backup = grid[row][col]
            grid[row][col] = 0

            # Check for uniqueness: use a solver variant that counts solutions
            solutions = self.count_solutions(copy.deepcopy(grid), 0)
            if solutions != 1:
                grid[row][col] = backup
                attempts -= 1
            else:
                self.grid = grid
        return grid

    def count_solutions(self, grid, count):
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            count = self.count_solutions(grid, count)
                            if count > 1:  # Early stop if more than 1 solution
                                return count
                            grid[row][col] = 0
                    return count
        return count + 1


if __name__ == "__main__":
    gen = SudokuGenerator()
    full_grid = gen.generate_full_grid()
    print("Generated full solution grid:")
    for row in full_grid:
        print([num if num != 0 else ' ' for num in row])

    puzzle = gen.remove_numbers(attempts=5)
    print("\nGenerated puzzle grid:")
    for row in puzzle:
        print([num if num != 0 else ' ' for num in row])
