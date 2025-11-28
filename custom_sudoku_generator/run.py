import random
import copy
import os
import json
import importlib.util
import time
from datetime import datetime
from base_rule import BaseRule

# Generation settings per difficulty level
# Hard: 5 attempts x 10s timeout each
HARD_ATTEMPT_COUNT = 3
HARD_ATTEMPT_TIMEOUT = 10
HARD_REMOVAL_TARGET = 100  # Target all cells to remove for hard

# Medium: 10 attempts x 2s timeout each
MEDIUM_ATTEMPT_COUNT = 5
MEDIUM_ATTEMPT_TIMEOUT = 2
MEDIUM_REMOVAL_TARGET = 0.67  # Target 66% cells to remove for medium

# Easy: 10 attempts x 1s timeout each
EASY_ATTEMPT_COUNT = 5
EASY_ATTEMPT_TIMEOUT = 1
EASY_REMOVAL_TARGET = 0.50  # Target 50% cells to remove for easy

# Priority cell settings
PRIORITY_CELL_DROP_RATE = 0.20  # Randomly drop 20% of priority cells for variety


class SudokuGenerator:
    def __init__(self, size=9, box_size=3, custom_rule=None):
        self.size = size              # 9 for classic Sudoku
        self.box_size = box_size      # 3 for classic Sudoku (3x3 boxes)
        self.grid = [[0]*size for _ in range(size)]
        self.custom_rule_instance = custom_rule if custom_rule else BaseRule(size, box_size)
        self.timeout_start = None
        self.timeout_duration = HARD_ATTEMPT_TIMEOUT  # Default timeout per attempt
        self.timed_out = False


    def is_valid(self, grid, row, col, num):
        # Standard Sudoku rules - row and column constraints (always apply)
        if any(grid[row][i] == num for i in range(self.size)):
            return False
        if any(grid[i][col] == num for i in range(self.size)):
            return False

        # Standard box constraint (only if the rule uses standard boxes)
        if self.custom_rule_instance.use_standard_boxes:
            box_row_start = (row // self.box_size) * self.box_size
            box_col_start = (col // self.box_size) * self.box_size
            for r in range(box_row_start, box_row_start + self.box_size):
                for c in range(box_col_start, box_col_start + self.box_size):
                    if grid[r][c] == num:
                        return False

        # Custom rule checks
        if not self.custom_rule(grid, row, col, num):
            return False

        return True

    def custom_rule(self, grid, row, col, num):
        """
        Delegate to the custom rule instance for validation.
        """
        return self.custom_rule_instance.validate(grid, row, col, num)

    def check_timeout(self):
        """
        Check if the timeout has been exceeded.
        Returns True if timeout has been exceeded, False otherwise.
        """
        if self.timeout_start is None:
            return False
        elapsed = time.time() - self.timeout_start
        if elapsed > self.timeout_duration:
            if not self.timed_out:
                print(f"\n⏱️  Timeout reached ({self.timeout_duration}s). Saving best puzzle found so far...")
                self.timed_out = True
            return True
        return False


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

        # Check if the rule supports pre-filling (e.g., magic square)
        if hasattr(self.custom_rule_instance, 'pre_fill_grid'):
            success = self.custom_rule_instance.pre_fill_grid(self.grid)
            if not success:
                print("Warning: Pre-fill failed, but continuing anyway...")

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

    def count_filled_cells(self, grid):
        """Count the number of filled (non-zero) cells in the grid."""
        return sum(1 for row in grid for cell in row if cell != 0)

    def reset_timeout(self):
        """Reset the timeout tracking for a new generation attempt."""
        self.timeout_start = None
        self.timed_out = False

    def generate_with_multi_attempts(self, solution_grid, difficulty='hard'):
        """
        Generate a puzzle using the new multi-attempt approach for all difficulty levels.
        
        For each attempt:
        1. Start with the full solution
        2. Try to remove the target percentage of numbers within the timeout
        3. Save the result
        
        After all attempts, return the puzzle with the least remaining numbers.
        
        Args:
            solution_grid: The complete solution grid to start from
            difficulty: 'easy', 'medium', or 'hard'
        
        Returns:
            The best puzzle grid (with fewest remaining clues)
        """
        # Set parameters based on difficulty
        if difficulty == 'easy':
            attempt_count = EASY_ATTEMPT_COUNT
            attempt_timeout = EASY_ATTEMPT_TIMEOUT
            target_removal_percentage = EASY_REMOVAL_TARGET
        elif difficulty == 'medium':
            attempt_count = MEDIUM_ATTEMPT_COUNT
            attempt_timeout = MEDIUM_ATTEMPT_TIMEOUT
            target_removal_percentage = MEDIUM_REMOVAL_TARGET
        else:  # 'hard'
            attempt_count = HARD_ATTEMPT_COUNT
            attempt_timeout = HARD_ATTEMPT_TIMEOUT
            target_removal_percentage = HARD_REMOVAL_TARGET
        
        total_cells = self.size * self.size
        target_empty_cells = int(total_cells * target_removal_percentage)
        
        all_attempts = []
        
        print(f"  Running {attempt_count} attempts with {attempt_timeout}s timeout each...")
        print(f"  Target: Remove {int(target_removal_percentage * 100)}% of cells ({target_empty_cells} cells)")
        
        for attempt_num in range(attempt_count):
            print(f"  Attempt {attempt_num + 1}/{attempt_count}...")
            
            # Reset for this attempt
            self.grid = copy.deepcopy(solution_grid)
            self.reset_timeout()
            self.timeout_duration = attempt_timeout
            self.timeout_start = time.time()
            
            # Try to remove numbers with this timeout
            puzzle_grid = self._remove_numbers_with_target(
                target_empty_cells=target_empty_cells,
                max_failed_attempts=100  # Allow many attempts within the timeout
            )
            
            clues_remaining = self.count_filled_cells(puzzle_grid)
            all_attempts.append((clues_remaining, copy.deepcopy(puzzle_grid)))
            print(f"    → {clues_remaining} clues remaining")
        
        # Pick the best attempt (least remaining clues)
        all_attempts.sort(key=lambda x: x[0])
        best_clues, best_puzzle = all_attempts[0]
        
        print(f"  Best result: {best_clues} clues remaining")
        
        return best_puzzle

    def _remove_numbers_with_target(self, target_empty_cells, max_failed_attempts=100):
        """
        Remove numbers from the grid while maintaining a unique solution.
        Uses timeout-based termination.
        
        Args:
            target_empty_cells: Target number of empty cells
            max_failed_attempts: Number of consecutive failed removal attempts before stopping
        
        Returns:
            The puzzle grid with numbers removed
        """
        grid = copy.deepcopy(self.grid)
        total_cells = self.size * self.size
        
        # Get priority cells from the rule (cells that should be removed first)
        priority_cells = []
        if hasattr(self.custom_rule_instance, 'get_priority_removal_cells'):
            priority_cells = self.custom_rule_instance.get_priority_removal_cells()
            priority_cells = [(r, c) for r, c in priority_cells if grid[r][c] != 0]
            # Randomly drop some priority cells to add variety
            priority_cells = [cell for cell in priority_cells if random.random() > PRIORITY_CELL_DROP_RATE]
            random.shuffle(priority_cells)

        cells_removed = 0
        priority_index = 0
        failed_attempts = 0
        max_iterations = total_cells * 10  # Safeguard against unexpected infinite loop
        iterations = 0

        while failed_attempts < max_failed_attempts and iterations < max_iterations:
            iterations += 1
            
            # Check timeout
            if self.check_timeout():
                break

            # Check if we've reached our target
            current_empty = total_cells - self.count_filled_cells(grid)
            if current_empty >= target_empty_cells:
                break
            
            # First try priority cells, then fall back to random cells
            if priority_index < len(priority_cells):
                row, col = priority_cells[priority_index]
                priority_index += 1
            else:
                # Random selection after priority cells are exhausted
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                # Find a filled cell
                max_tries = 100
                tries = 0
                while grid[row][col] == 0 and tries < max_tries:
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, self.size - 1)
                    tries += 1
                if tries >= max_tries:
                    break  # No more cells to remove

            # Skip if cell is already empty
            if grid[row][col] == 0:
                continue

            backup = grid[row][col]
            grid[row][col] = 0

            # Check for uniqueness: use a solver variant that counts solutions
            solutions = self.count_solutions(copy.deepcopy(grid), 0)
            if solutions != 1:
                grid[row][col] = backup
                failed_attempts += 1
            else:
                self.grid = grid
                cells_removed += 1
                failed_attempts = 0  # Reset failed attempts on success
                
        return grid

    # Remove clues while ensuring unique solution
    def remove_numbers(self, attempts=1, difficulty='hard'):
        """
        Remove numbers from the grid while maintaining a unique solution.
        
        Args:
            attempts: Number of failed removal attempts before stopping (used for hard difficulty)
            difficulty: Difficulty level - 'easy', 'medium', or 'hard'
                - 'easy': Stop after ~50% of numbers have been removed
                - 'medium': Stop after ~75% of numbers have been removed
                - 'hard': Continue until no more numbers can be removed (no early termination)
        
        Returns:
            The puzzle grid with numbers removed
        """
        # Start timeout tracking
        if self.timeout_start is None:
            self.timeout_start = time.time()

        grid = copy.deepcopy(self.grid)
        total_cells = self.size * self.size  # 81 for 9x9 grid
        
        # Calculate removal targets based on difficulty
        if difficulty == 'easy':
            target_empty_cells = int(total_cells * 0.50)  # ~40 cells empty
        elif difficulty == 'medium':
            target_empty_cells = int(total_cells * 0.70)  # ~57 cells empty
        else:  # 'hard' - no early termination
            target_empty_cells = int(total_cells * 0.90)  # ~73 cells empty

        # Get priority cells from the rule (cells that should be removed first)
        priority_cells = []
        if hasattr(self.custom_rule_instance, 'get_priority_removal_cells'):
            priority_cells = self.custom_rule_instance.get_priority_removal_cells()
            # Filter to only cells that are currently filled
            priority_cells = [(r, c) for r, c in priority_cells if grid[r][c] != 0]
            # Randomly drop some priority cells to add variety
            priority_cells = [cell for cell in priority_cells if random.random() > PRIORITY_CELL_DROP_RATE]
            random.shuffle(priority_cells)  # Randomize order within priority cells

        cells_attempted = 0
        priority_index = 0
        cells_removed = 0

        while attempts > 0:
            # Check timeout
            if self.check_timeout():
                break

            # Check if we've reached our target for easy/medium difficulty
            if difficulty in ('easy', 'medium') and cells_removed >= target_empty_cells:
                break
            
            # First try priority cells, then fall back to random cells
            if priority_index < len(priority_cells):
                row, col = priority_cells[priority_index]
                priority_index += 1
            else:
                # Random selection after priority cells are exhausted
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                # Find a filled cell
                max_tries = 100
                tries = 0
                while grid[row][col] == 0 and tries < max_tries:
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, self.size - 1)
                    tries += 1
                if tries >= max_tries:
                    break  # No more cells to remove

            # Skip if cell is already empty
            if grid[row][col] == 0:
                continue

            backup = grid[row][col]
            grid[row][col] = 0

            # Check for uniqueness: use a solver variant that counts solutions
            solutions = self.count_solutions(copy.deepcopy(grid), 0)
            if solutions != 1:
                grid[row][col] = backup
                attempts -= 1
            else:
                self.grid = grid
                cells_removed += 1
        return grid

    def count_solutions(self, grid, count):
        # Check timeout before continuing
        if self.check_timeout():
            return count

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


def generate_sudoku_for_rule(rule_folder, difficulty_attempts=None, difficulty='hard'):
    """
    Generate a Sudoku puzzle for a specific rule folder.

    Args:
        rule_folder: Path to the folder containing the rule
        difficulty_attempts: Number of attempts to remove cells (higher = harder).
                           If None, uses smart defaults based on rule complexity.
        difficulty: Difficulty level - 'easy', 'medium', or 'hard'
                   - 'easy': Stop after ~50% of numbers have been removed
                   - 'medium': Stop after ~75% of numbers have been removed
                   - 'hard': Aims for < 12 clues, retries within 30s if not achieved

    Returns:
        tuple: (puzzle_grid, solution_grid)
    """
    # Load the custom rule
    custom_rule = load_custom_rule(rule_folder)

    print(f"\nGenerating Sudoku with rule: {custom_rule.name}")
    print(f"Description: {custom_rule.description}")
    print(f"Difficulty: {difficulty}")

    # Use smart defaults if not specified
    if difficulty_attempts is None:
        # For hard mode, use many attempts to try to remove as many cells as possible
        if difficulty == 'hard':
            difficulty_attempts = 100  # Many attempts for hard mode to maximize cell removal
        # Check if rule is highly restrictive (e.g., non-consecutive)
        elif hasattr(custom_rule, 'is_highly_restrictive') and custom_rule.is_highly_restrictive:
            difficulty_attempts = 1 # Very few attempts for highly restrictive rules
        # Reverse generation rules have complex constraints - use fewer attempts
        elif custom_rule.supports_reverse_generation():
            difficulty_attempts = 2  # Fewer attempts for complex rules
        else:
            difficulty_attempts = 2  # Standard attempts for simple rules

    # Check if this rule supports reverse generation
    if custom_rule.supports_reverse_generation():
        print("Using REVERSE GENERATION mode (solution first, then constraints)...")
        return generate_sudoku_reverse(custom_rule, rule_folder, difficulty_attempts, difficulty=difficulty)
    else:
        print("Using FORWARD GENERATION mode (constraints first, then solution)...")
        return generate_sudoku_forward(custom_rule, rule_folder, difficulty_attempts, difficulty=difficulty)


def generate_sudoku_forward(custom_rule, rule_folder, difficulty_attempts=5, difficulty='hard'):
    """
    Traditional generation: Start with constraints, generate a solution that satisfies them.

    Args:
        custom_rule: The custom rule instance
        rule_folder: Path to save the puzzle
        difficulty_attempts: Number of attempts to remove cells
        difficulty: Difficulty level - 'easy', 'medium', or 'hard'
            - 'easy': 10 attempts x 1s timeout each, target 50% removal, pick best
            - 'medium': 10 attempts x 2s timeout each, target 66% removal, pick best
            - 'hard': 5 attempts x 10s timeout each, target 90% removal, pick best

    Returns:
        tuple: (puzzle_grid, solution_grid)
    """
    # Create generator with the custom rule
    gen = SudokuGenerator(custom_rule=custom_rule)
    
    # Generate full solution
    print("Generating full solution...")
    solution_grid = gen.generate_full_grid()
    
    # Use multi-attempt approach for all difficulty levels
    print(f"Creating puzzle using multi-attempt approach (difficulty: {difficulty})...")
    puzzle_grid = gen.generate_with_multi_attempts(solution_grid, difficulty=difficulty)
    
    filled_cells = gen.count_filled_cells(puzzle_grid)
    print(f"📊 Final puzzle has {filled_cells} clues remaining")
    
    gen.save_puzzle(rule_folder, puzzle_grid, solution_grid)
    return puzzle_grid, solution_grid


def generate_sudoku_reverse(custom_rule, rule_folder, difficulty_attempts=1, max_regeneration_attempts=10, difficulty='hard'):
    """
    Reverse generation: Generate a standard Sudoku solution first, then derive constraints from it.

    This is much faster for complex rules like Killer, Sandwich, Arrow, etc.
    If constraints cannot be derived (e.g., not enough non-overlapping lines),
    regenerates a new solution and retries.

    Args:
        custom_rule: The custom rule instance (must support reverse generation)
        rule_folder: Path to save the puzzle
        difficulty_attempts: Number of attempts to remove cells
        max_regeneration_attempts: Maximum number of times to regenerate the solution
        difficulty: Difficulty level - 'easy', 'medium', or 'hard'
            - 'easy': 10 attempts x 1s timeout each, target 50% removal, pick best
            - 'medium': 10 attempts x 2s timeout each, target 66% removal, pick best
            - 'hard': 5 attempts x 10s timeout each, target 90% removal, pick best

    Returns:
        tuple: (puzzle_grid, solution_grid) or (None, None) if all attempts fail
    """
    for attempt in range(max_regeneration_attempts):
        # First, generate a standard Sudoku solution (no custom constraints)
        print(f"Step 1: Generating standard Sudoku solution (attempt {attempt + 1}/{max_regeneration_attempts})...")
        base_gen = SudokuGenerator(custom_rule=BaseRule())
        solution_grid = base_gen.generate_full_grid()

        print("Step 2: Deriving constraints from solution...")
        # Derive constraints from the solution
        if custom_rule.derive_constraints_from_solution(solution_grid):
            print(f"Step 3: Creating puzzle by removing numbers (difficulty: {difficulty})...")
            # Now create a generator with the custom rule that has derived constraints
            gen = SudokuGenerator(custom_rule=custom_rule)
            gen.grid = copy.deepcopy(solution_grid)
            
            # Use multi-attempt approach for all difficulty levels
            puzzle_grid = gen.generate_with_multi_attempts(solution_grid, difficulty=difficulty)
            
            filled_cells = gen.count_filled_cells(puzzle_grid)
            print(f"📊 Final puzzle has {filled_cells} clues remaining")
            
            gen.save_puzzle(rule_folder, puzzle_grid, solution_grid)
            return puzzle_grid, solution_grid
        else:
            print(f"  Constraints could not be derived, regenerating solution...")

    print(f"ERROR: Failed to derive constraints after {max_regeneration_attempts} attempts!")
    return None, None


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
    from tqdm import tqdm
    # Discover rules first
    rule_folders = discover_rules()

    # Check for special flags
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        print("=== Sudoku Generator - Generating All Rules ===\n")
        for folder in tqdm(rule_folders):
            generate_sudoku_for_rule(folder)
            print("\n" + "="*60 + "\n")
    elif len(sys.argv) > 2 and sys.argv[1] == "--index":
        idx = int(sys.argv[2]) - 1
        if 0 <= idx < len(rule_folders):
            difficulty = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            generate_sudoku_for_rule(rule_folders[idx], difficulty)
        else:
            print(f"Error: Invalid index. Choose between 1 and {len(rule_folders)}")
    elif len(sys.argv) > 1:
        # Check if a specific rule folder is provided
        rule_folder = sys.argv[1]
        difficulty = int(sys.argv[2]) if len(sys.argv) > 2 else 1

        if os.path.exists(rule_folder):
            generate_sudoku_for_rule(rule_folder, difficulty)
        else:
            print(f"Error: Rule folder '{rule_folder}' not found")
    else:
        # List available rules
        print("=== Sudoku Generator - Modular System ===\n")

        if not rule_folders:
            print("No rule folders found. Generating a basic Sudoku...")
            gen = SudokuGenerator()
            full_grid = gen.generate_full_grid()
            print("\nGenerated full solution grid:")
            for row in full_grid:
                print([num for num in row])

            puzzle = gen.remove_numbers(attempts=1)
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
