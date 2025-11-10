import random
import copy
import os
import json
import importlib.util
from datetime import datetime
from base_rule import BaseRule

class SudokuGenerator:
    def __init__(self, size=9, box_size=3, custom_rule=None):
        self.size = size              # 9 for classic Sudoku
        self.box_size = box_size      # 3 for classic Sudoku (3x3 boxes)
        self.grid = [[0]*size for _ in range(size)]
        self.custom_rule_instance = custom_rule if custom_rule else BaseRule(size, box_size)


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
        """
        Delegate to the custom rule instance for validation.
        """
        return self.custom_rule_instance.validate(grid, row, col, num)


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

    def save_puzzle(self, output_folder, puzzle_grid, solution_grid):
        """
        Save the puzzle and solution to the specified folder.

        Args:
            output_folder: Folder path where files will be saved
            puzzle_grid: The puzzle grid (with some cells empty)
            solution_grid: The complete solution grid
        """
        os.makedirs(output_folder, exist_ok=True)

        # Save puzzle
        puzzle_path = os.path.join(output_folder, "sudoku.txt")
        with open(puzzle_path, 'w') as f:
            for row in puzzle_grid:
                f.write(str(row) + '\n')

        # Save solution
        solution_path = os.path.join(output_folder, "solution.txt")
        with open(solution_path, 'w') as f:
            for row in solution_grid:
                f.write(str(row) + '\n')

        # Save metadata
        metadata = {
            "rule": self.custom_rule_instance.get_metadata(),
            "generated_at": datetime.now().isoformat(),
            "size": self.size,
            "box_size": self.box_size
        }
        metadata_path = os.path.join(output_folder, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"Puzzle saved to: {output_folder}")
        print(f"  - Puzzle: {puzzle_path}")
        print(f"  - Solution: {solution_path}")
        print(f"  - Metadata: {metadata_path}")


def load_custom_rule(rule_folder):
    """
    Load a custom rule from a folder.

    Args:
        rule_folder: Path to the folder containing rule.py

    Returns:
        An instance of the custom rule class
    """
    rule_file = os.path.join(rule_folder, "rule.py")

    if not os.path.exists(rule_file):
        print(f"Warning: No rule.py found in {rule_folder}")
        return BaseRule()

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("custom_rule_module", rule_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Try to call the create_rule factory function
    if hasattr(module, 'create_rule'):
        return module.create_rule()

    # Look for a class that inherits from BaseRule
    for item_name in dir(module):
        item = getattr(module, item_name)
        if isinstance(item, type) and issubclass(item, BaseRule) and item is not BaseRule:
            return item()

    print(f"Warning: No valid rule class found in {rule_file}")
    return BaseRule()


def generate_sudoku_for_rule(rule_folder, difficulty_attempts=5):
    """
    Generate a Sudoku puzzle for a specific rule folder.

    Args:
        rule_folder: Path to the folder containing the rule
        difficulty_attempts: Number of attempts to remove cells (higher = harder)

    Returns:
        tuple: (puzzle_grid, solution_grid)
    """
    # Load the custom rule
    custom_rule = load_custom_rule(rule_folder)

    print(f"\nGenerating Sudoku with rule: {custom_rule.name}")
    print(f"Description: {custom_rule.description}")

    # Create generator with the custom rule
    gen = SudokuGenerator(custom_rule=custom_rule)

    # Generate full solution
    print("Generating full solution...")
    solution_grid = gen.generate_full_grid()

    # Create puzzle by removing numbers
    print(f"Creating puzzle (difficulty attempts: {difficulty_attempts})...")
    puzzle_grid = gen.remove_numbers(attempts=difficulty_attempts)

    # Save the puzzle
    gen.save_puzzle(rule_folder, puzzle_grid, solution_grid)

    return puzzle_grid, solution_grid


def discover_rules(base_folder=None):
    """
    Discover all rule folders in the base folder.

    Args:
        base_folder: Base folder to search for rule folders (defaults to current directory)

    Returns:
        list: List of rule folder paths
    """
    if base_folder is None:
        base_folder = os.path.dirname(os.path.abspath(__file__))

    rule_folders = []

    for item in os.listdir(base_folder):
        item_path = os.path.join(base_folder, item)
        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "rule.py")):
            rule_folders.append(item_path)

    return rule_folders


if __name__ == "__main__":
    import sys

    # Check if a specific rule folder is provided
    if len(sys.argv) > 1:
        rule_folder = sys.argv[1]
        difficulty = int(sys.argv[2]) if len(sys.argv) > 2 else 5

        if os.path.exists(rule_folder):
            generate_sudoku_for_rule(rule_folder, difficulty)
        else:
            print(f"Error: Rule folder '{rule_folder}' not found")
    else:
        # Discover and generate for all rules
        print("=== Sudoku Generator - Modular System ===\n")

        rule_folders = discover_rules()

        if not rule_folders:
            print("No rule folders found. Generating a basic Sudoku...")
            gen = SudokuGenerator()
            full_grid = gen.generate_full_grid()
            print("\nGenerated full solution grid:")
            for row in full_grid:
                print([num for num in row])

            puzzle = gen.remove_numbers(attempts=5)
            print("\nGenerated puzzle grid:")
            for row in puzzle:
                print([num for num in row])
        else:
            print(f"Found {len(rule_folders)} rule folder(s):\n")
            for i, folder in enumerate(rule_folders, 1):
                print(f"{i}. {os.path.basename(folder)}")

            print("\nOptions:")
            print("  - Run with specific folder: python run.py <rule_folder_path> [difficulty]")
            print("  - Generate for all: python run.py --all")
            print("  - Generate for specific folder from list: python run.py --index <number>")

            if len(sys.argv) > 1 and sys.argv[1] == "--all":
                for folder in rule_folders:
                    generate_sudoku_for_rule(folder)
                    print("\n" + "="*60 + "\n")
            elif len(sys.argv) > 2 and sys.argv[1] == "--index":
                idx = int(sys.argv[2]) - 1
                if 0 <= idx < len(rule_folders):
                    difficulty = int(sys.argv[3]) if len(sys.argv) > 3 else 5
                    generate_sudoku_for_rule(rule_folders[idx], difficulty)
                else:
                    print(f"Error: Invalid index. Choose between 1 and {len(rule_folders)}")
