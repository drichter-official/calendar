# Modular Sudoku Generator

A flexible, extensible Sudoku generator that supports custom rules and constraints.

## Structure

```
custom_sudoku_generator/
├── run.py                  # Main generator script
├── base_rule.py            # Base class for custom rules
├── README.md               # This file
└── <rule_name>/            # Custom rule folders
    ├── rule.py             # Rule implementation
    ├── sudoku.txt          # Generated puzzle (auto-generated)
    ├── solution.txt        # Generated solution (auto-generated)
    └── metadata.json       # Rule metadata (auto-generated)
```

## How It Works

### 1. Creating a Custom Rule

To create a custom Sudoku rule, create a new folder and add a `rule.py` file that inherits from `BaseRule`:

```python
from base_rule import BaseRule

class MyCustomRule(BaseRule):
    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "My Custom Rule"
        self.description = "Description of what makes this rule unique"
    
    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) is valid according to your rule.
        
        Args:
            grid: Current state of the Sudoku grid (2D list)
            row: Row index (0-based)
            col: Column index (0-based)
            num: Number to place (1-9)
            
        Returns:
            True if placement is valid, False otherwise
        """
        # Your custom validation logic here
        # Return False if the rule is violated
        return True

# Factory function (optional but recommended)
def create_rule(size=9, box_size=3):
    return MyCustomRule(size, box_size)
```

### 2. Example: Knight's Rule

The `sudoku_knights_rule` folder contains a working example. The Knight's Rule prevents two cells that are a chess knight's move apart from containing the same digit.

### 3. Generating Sudokus

#### Generate for a specific rule:
```bash
python run.py sudoku_knights_rule/
```

#### Generate with custom difficulty (higher = harder):
```bash
python run.py sudoku_knights_rule/ 10
```

#### Discover all available rules:
```bash
python run.py
```

#### Generate for all rules at once:
```bash
python run.py --all
```

#### Generate by index:
```bash
python run.py --index 1
```

## Creating Your Own Rules

### Example 1: Diagonal Rule (No repeated digits on diagonals)

Create folder `sudoku_diagonal_rule/` with `rule.py`:

```python
from base_rule import BaseRule

class DiagonalRule(BaseRule):
    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Diagonal Rule"
        self.description = "No repeated digits on main diagonals"
    
    def validate(self, grid, row, col, num):
        # Check main diagonal (top-left to bottom-right)
        if row == col:
            for i in range(self.size):
                if grid[i][i] == num:
                    return False
        
        # Check anti-diagonal (top-right to bottom-left)
        if row + col == self.size - 1:
            for i in range(self.size):
                if grid[i][self.size - 1 - i] == num:
                    return False
        
        return True

def create_rule(size=9, box_size=3):
    return DiagonalRule(size, box_size)
```

### Example 2: King's Rule (No adjacent cells with same digit)

Create folder `sudoku_kings_rule/` with `rule.py`:

```python
from base_rule import BaseRule

class KingsRule(BaseRule):
    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "King's Rule"
        self.description = "No adjacent cells (including diagonals) can have the same digit"
    
    def validate(self, grid, row, col, num):
        # Check all 8 surrounding cells
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if grid[nr][nc] == num:
                        return False
        return True

def create_rule(size=9, box_size=3):
    return KingsRule(size, box_size)
```

## Output Files

When you generate a Sudoku for a rule, the following files are created in the rule folder:

- **sudoku.txt**: The puzzle with some cells removed
- **solution.txt**: The complete solution
- **metadata.json**: Information about the rule and generation parameters

## API Usage

You can also use the generator programmatically:

```python
from run import SudokuGenerator, load_custom_rule

# Load a custom rule
custom_rule = load_custom_rule("sudoku_knights_rule")

# Create generator
gen = SudokuGenerator(custom_rule=custom_rule)

# Generate solution
solution = gen.generate_full_grid()

# Create puzzle
puzzle = gen.remove_numbers(attempts=10)

# Save to folder
gen.save_puzzle("output_folder/", puzzle, solution)
```

## Difficulty Levels

The `difficulty_attempts` parameter controls how many cells are removed:
- **5** (default): Easy
- **10-20**: Medium
- **30+**: Hard (may take longer to generate)

Note: Higher difficulty doesn't always guarantee a harder puzzle, as the algorithm ensures unique solutions.

## Tips for Creating Rules

1. **Start simple**: Test your rule logic with simple cases first
2. **Consider performance**: Complex rules can slow down generation significantly
3. **Test validity**: Ensure your rule doesn't make the puzzle unsolvable
4. **Document well**: Use clear names and descriptions for your rules
5. **Use the factory pattern**: Implement `create_rule()` for easier instantiation

## Troubleshooting

- **Generation takes too long**: Try reducing the difficulty or simplifying your rule
- **No valid puzzle generated**: Your rule might be too restrictive
- **Import errors**: Ensure `base_rule.py` is in the parent directory of your rule folder

