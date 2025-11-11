# Quick Reference Guide for Developers

## Adding a New Rule Variant

### Step 1: Create Rule Folder
```bash
mkdir sudoku_myrule_rule
cd sudoku_myrule_rule
touch rule.py
```

### Step 2: Implement the Rule Class

```python
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class MyRule(BaseRule):
    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "My Custom Rule"
        self.description = "Description of the rule"
        
        # For rules that REPLACE standard 3x3 boxes (rare):
        # self.use_standard_boxes = False
        
    def validate(self, grid, row, col, num):
        """
        Validate if placing 'num' at (row, col) is allowed.
        Return False if the rule is violated.
        """
        # Your validation logic here
        return True


# Factory function
def create_rule(size=9, box_size=3):
    return MyRule(size, box_size)
```

### Step 3: Decide on Generation Mode

#### Option A: Forward Generation (Simple Rules)
Use when constraints are geometric or positional:
- Diagonal constraints
- Knight's/King's move
- Windoku
- Fixed regions

**No additional code needed** - just implement `validate()`

#### Option B: Reverse Generation (Complex Rules)
Use when constraints are calculated from values:
- Sum-based constraints (Killer, Arrow, Sandwich)
- Sequence-based (Thermo, Renban)
- Calculated clues

```python
def supports_reverse_generation(self):
    return True

def derive_constraints_from_solution(self, solution_grid):
    """
    Create constraints from a complete solution.
    """
    print("  Deriving constraints from solution...")
    
    # Your constraint derivation logic here
    # Example: self.my_constraints = [...]
    
    print(f"  Created {len(self.my_constraints)} constraints")
    return True
```

### Step 4: Add Metadata (If Rule Has Visual Elements)

```python
def get_metadata(self):
    """Export metadata for visualization."""
    metadata = super().get_metadata()
    
    # Add your visual elements
    metadata['my_regions'] = self.regions
    metadata['my_lines'] = self.lines
    metadata['generation_mode'] = 'reverse' if self.supports_reverse_generation() else 'forward'
    
    return metadata
```

### Step 5: Test Your Rule

```bash
python run.py sudoku_myrule_rule
```

Check the output:
- ✓ Puzzle generated successfully?
- ✓ Metadata includes all visual elements?
- ✓ Generation time reasonable?

---

## Decision Tree: When to Use What

```
Does your rule replace standard 3x3 boxes?
├─ YES → Set use_standard_boxes = False
│        (e.g., Jigsaw with irregular regions)
└─ NO  → Keep default (use_standard_boxes = True)

Are constraints calculated from digit values?
├─ YES → Use REVERSE generation
│        │
│        ├─ Sum-based? (Killer, Arrow, Sandwich)
│        ├─ Sequence-based? (Thermo, Renban, Whisper)
│        └─ Calculated clues? (Skyscraper sums)
│
└─ NO  → Use FORWARD generation
         │
         ├─ Geometric? (Diagonal, Windoku)
         ├─ Positional? (Knight's, King's)
         └─ Fixed regions? (Asterisk, Argyle)

Does your rule have visual elements?
├─ YES → Override get_metadata()
│        Export: regions, lines, cells, constraints
└─ NO  → Use default metadata
```

---

## Common Patterns

### Pattern 1: Region-Based Rules
```python
class MyRegionRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.regions = [
            [(0,0), (0,1), (1,0)],  # Region 1
            [(0,2), (1,1), (1,2)],  # Region 2
            # ...
        ]
    
    def validate(self, grid, row, col, num):
        # Find which region this cell is in
        for region in self.regions:
            if (row, col) in region:
                # Check no duplicate in region
                for r, c in region:
                    if grid[r][c] == num:
                        return False
        return True
```

### Pattern 2: Line-Based Rules
```python
class MyLineRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.lines = [
            [(0,0), (1,1), (2,2)],  # Line 1
            [(0,2), (1,2), (2,2)],  # Line 2
        ]
    
    def validate(self, grid, row, col, num):
        # Check each line this cell is part of
        for line in self.lines:
            if (row, col) in line:
                # Apply line constraint
                # ...
        return True
```

### Pattern 3: Sum-Based Rules (Use Reverse!)
```python
class MySumRule(BaseRule):
    def supports_reverse_generation(self):
        return True
    
    def derive_constraints_from_solution(self, solution_grid):
        self.constraints = []
        # Derive sum constraints from solution
        for region in self.find_regions():
            total = sum(solution_grid[r][c] for r, c in region)
            self.constraints.append((region, total))
        return True
    
    def validate(self, grid, row, col, num):
        # Check sum constraints
        for region, target in self.constraints:
            if (row, col) in region:
                # Validate sum
                # ...
        return True
```

---

## Checklist

### Before Committing a New Rule
- [ ] Rule class inherits from `BaseRule`
- [ ] `validate()` method implemented
- [ ] `create_rule()` factory function exists
- [ ] Generation mode chosen (forward/reverse)
- [ ] If reverse: `supports_reverse_generation()` and `derive_constraints_from_solution()` implemented
- [ ] If visual elements: `get_metadata()` implemented
- [ ] If replaces boxes: `use_standard_boxes = False` set
- [ ] Rule tested with `python run.py sudoku_myrule_rule`
- [ ] Metadata verified in `metadata.json`
- [ ] Generation time acceptable (< 30s)

---

## Performance Guidelines

### Target Generation Times
- **Simple rules** (forward): < 10 seconds
- **Complex rules** (reverse): < 3 seconds
- **Very complex rules**: < 30 seconds

### If Generation is Slow
1. Consider switching to reverse generation
2. Optimize validation logic (early exits)
3. Reduce constraint complexity
4. Use caching for repeated checks

---

## Common Mistakes to Avoid

### ❌ DON'T: Mix standard boxes with replacement regions
```python
# WRONG: Jigsaw with standard boxes still enabled
class JigsawRule(BaseRule):
    def __init__(self):
        super().__init__()
        # use_standard_boxes defaults to True - WRONG for Jigsaw!
        self.jigsaw_regions = [...]
```

### ✅ DO: Disable standard boxes when replacing them
```python
# CORRECT: Jigsaw disables standard boxes
class JigsawRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.use_standard_boxes = False  # ← Important!
        self.jigsaw_regions = [...]
```

### ❌ DON'T: Use forward generation for sum-based rules
```python
# WRONG: Trying to satisfy predefined sums
class KillerRule(BaseRule):
    def __init__(self):
        self.cages = [(15, [...]), (10, [...])]  # Predefined sums
    # This will be VERY slow or fail!
```

### ✅ DO: Use reverse generation for sum-based rules
```python
# CORRECT: Derive sums from solution
class KillerRule(BaseRule):
    def supports_reverse_generation(self):
        return True
    
    def derive_constraints_from_solution(self, solution_grid):
        # Create cages, calculate sums from solution
        for cage in random_cages:
            total = sum(solution_grid[r][c] for r, c in cage)
            self.cages.append((total, cage))
        return True
```

### ❌ DON'T: Forget metadata for visual rules
```python
# WRONG: No way to visualize the thermometers
class ThermoRule(BaseRule):
    def __init__(self):
        self.thermometers = [...]
    # Missing get_metadata()!
```

### ✅ DO: Export visual elements in metadata
```python
# CORRECT: Thermometers included in metadata
class ThermoRule(BaseRule):
    def get_metadata(self):
        metadata = super().get_metadata()
        metadata['thermometers'] = self.thermometers
        return metadata
```

---

## Testing Commands

```bash
# Test a single rule
python run.py sudoku_myrule_rule

# Run performance test
python performance_test.py

# Check metadata
cat sudoku_myrule_rule/metadata.json

# Verify puzzle files
cat sudoku_myrule_rule/sudoku.txt
cat sudoku_myrule_rule/solution.txt
```

---

## Getting Help

- See `REVERSE_GENERATION.md` for reverse generation details
- See `STANDARD_BOX_OVERRIDE.md` for box override information
- See `IMPLEMENTATION_SUMMARY.md` for recent changes
- Look at existing rules for examples:
  - Simple: `sudoku_diagonal_rule`
  - Complex: `sudoku_killer_rule`
  - Regional: `sudoku_jigsaw_rule`
  - Line-based: `sudoku_thermo_rule`

---

**Happy Sudoku Creating! 🎉**

