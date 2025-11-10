# Modular Sudoku Generator - Quick Start Guide

## 🎯 What You Have Now

Your Sudoku generator is now **fully modular**! You can easily add new custom rules by simply creating a new folder with a `rule.py` file.

## 📁 Current Structure

```
custom_sudoku_generator/
├── run.py                      # Main generator script
├── base_rule.py                # Base class for all rules
├── examples.py                 # Usage examples
├── README.md                   # Detailed documentation
│
├── sudoku_knights_rule/        # Knight's Rule example
│   ├── rule.py                 # Rule implementation
│   ├── sudoku.txt              # Generated puzzle
│   ├── solution.txt            # Full solution
│   └── metadata.json           # Generation metadata
│
├── sudoku_diagonal_rule/       # Diagonal Rule (Sudoku X)
│   ├── rule.py
│   ├── sudoku.txt
│   ├── solution.txt
│   └── metadata.json
│
└── sudoku_kings_rule/          # King's Rule
    └── rule.py
```

## 🚀 Quick Usage

### 1. List All Available Rules
```bash
python run.py
```

### 2. Generate for a Specific Rule
```bash
python run.py sudoku_knights_rule/
```

### 3. Generate with Custom Difficulty
```bash
python run.py sudoku_diagonal_rule/ 10
```
Higher number = more cells removed (harder puzzle)

### 4. Generate by Index
```bash
python run.py --index 1
```

### 5. Generate All Rules at Once
```bash
python run.py --all
```

## 🎨 Creating a New Custom Rule

### Step 1: Create a Folder
```bash
mkdir sudoku_my_rule
```

### Step 2: Create `rule.py` in That Folder

```python
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class MyCustomRule(BaseRule):
    """
    Description of your rule.
    """
    
    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "My Custom Rule"
        self.description = "Brief description of what makes this unique"
    
    def validate(self, grid, row, col, num):
        """
        Return False if placing 'num' at (row, col) violates your rule.
        Return True if it's valid.
        
        Args:
            grid: 2D list representing the current sudoku state
            row: row index (0-8)
            col: column index (0-8)
            num: number to place (1-9)
        """
        # Your validation logic here
        # Example: check some condition
        # if condition_violated:
        #     return False
        
        return True


# Factory function (recommended)
def create_rule(size=9, box_size=3):
    return MyCustomRule(size, box_size)
```

### Step 3: Generate!
```bash
python run.py sudoku_my_rule/
```

## 📝 Included Rule Examples

### 1. **Knight's Rule**
No two cells a chess knight's move apart can contain the same digit.
```
Knight moves: L-shaped (2 squares in one direction, 1 in perpendicular)
```

### 2. **Diagonal Rule (Sudoku X)**
The two main diagonals must each contain digits 1-9 without repetition.
```
Adds constraint to diagonal cells
```

### 3. **King's Rule**
No two adjacent cells (including diagonals) can contain the same digit.
```
All 8 surrounding cells must have different values
```

## 🔧 Programmatic Usage

```python
from run import SudokuGenerator, load_custom_rule

# Load a rule
rule = load_custom_rule("sudoku_knights_rule")

# Create generator
gen = SudokuGenerator(custom_rule=rule)

# Generate solution and puzzle
solution = gen.generate_full_grid()
puzzle = gen.remove_numbers(attempts=10)

# Save to folder
gen.save_puzzle("output_folder/", puzzle, solution)
```

## 📊 Output Files

Each rule folder will contain (after generation):
- **sudoku.txt** - The puzzle with empty cells (0)
- **solution.txt** - The complete solution
- **metadata.json** - Rule info and generation timestamp

## 💡 Rule Ideas to Try

1. **Consecutive Rule**: Adjacent cells cannot have consecutive numbers
2. **Even/Odd Rule**: Certain cells must be even/odd
3. **Sum Rule**: Specific regions must sum to certain values
4. **Non-Consecutive Diagonal**: Diagonals can't have consecutive numbers
5. **Color Rule**: Cells of same "color" pattern have unique digits
6. **Thermometer Rule**: Numbers increase along certain paths
7. **Sandwich Rule**: Numbers between 1 and 9 sum to specific values

## 🎓 Examples Script

Run examples to see how to use the system programmatically:

```bash
python examples.py     # Run all examples
python examples.py 1   # Basic Sudoku
python examples.py 2   # With custom rule
python examples.py 3   # Discover rules
python examples.py 4   # Save to custom location
```

## 🔍 Troubleshooting

**Generation is slow?**
- Complex rules make generation harder
- Try lower difficulty (5 instead of 20)
- Some rule combinations may be very restrictive

**Rule not detected?**
- Ensure folder contains `rule.py`
- Check that your rule class inherits from `BaseRule`
- Verify the `create_rule()` factory function exists

**Import errors?**
- Make sure `base_rule.py` is in the parent directory
- Check the path manipulation code at the top of `rule.py`

## 📚 More Information

See `README.md` for detailed documentation and advanced usage.

---

**Happy Sudoku Generating! 🎲**

