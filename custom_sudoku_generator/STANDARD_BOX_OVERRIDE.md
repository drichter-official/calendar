# Standard Box Override Feature

## Overview

By default, Sudoku puzzles enforce standard 3x3 box constraints along with row and column constraints. However, some variants like **Jigsaw Sudoku** replace the standard boxes with their own regional constraints. This document explains how to disable standard box validation for such rules.

## The Problem

Before this fix, rules like Jigsaw Sudoku were incorrectly validating BOTH:
1. Standard 3x3 box constraints ❌
2. Custom irregular region constraints ✓

This made generation either impossible or produced invalid puzzles, since Jigsaw regions don't align with standard 3x3 boxes.

## The Solution

### New `use_standard_boxes` Flag

The `BaseRule` class now includes a `use_standard_boxes` flag (default: `True`):

```python
class BaseRule:
    def __init__(self, size=9, box_size=3):
        self.size = size
        self.box_size = box_size
        self.name = "Base Rule"
        self.description = "No custom rules applied"
        self.use_standard_boxes = True  # ← New flag
```

### Updated Validation Logic

The `SudokuGenerator.is_valid()` method now checks this flag:

```python
def is_valid(self, grid, row, col, num):
    # Standard Sudoku rules - row and column constraints (always apply)
    if any(grid[row][i] == num for i in range(self.size)):
        return False
    if any(grid[i][col] == num for i in range(self.size)):
        return False
    
    # Standard box constraint (ONLY if the rule uses standard boxes)
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
```

## Rules That Should Disable Standard Boxes

### ✓ Jigsaw Sudoku
**Reason**: Uses irregular regions that completely replace 3x3 boxes

```python
class JigsawRule(BaseRule):
    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.use_standard_boxes = False  # ← Disable standard boxes
        self.jigsaw_regions = [...]  # Define irregular regions
```

### Potential Future Variants

Other variants that might need this:
- **Irregular Sudoku** - Any variant with non-standard regions
- **Hyper Sudoku** - Might optionally replace boxes (depending on variant)
- **Custom Regional Variants** - User-defined region shapes

## Rules That Keep Standard Boxes

Most variants ADD constraints on top of standard Sudoku rules:

- ✓ **Diagonal/X Sudoku** - Adds diagonal constraints
- ✓ **Windoku** - Adds 4 extra overlapping 3x3 regions
- ✓ **Asterisk** - Adds asterisk pattern constraint
- ✓ **Knight's/King's Move** - Adds positional constraints
- ✓ **Killer Sudoku** - Adds cage sum constraints
- ✓ **Thermo** - Adds thermometer constraints
- ✓ **Arrow** - Adds arrow sum constraints
- ✓ **Sandwich** - Adds sandwich sum constraints

These all keep `use_standard_boxes = True` (default).

## Metadata Export

When a rule disables standard boxes, this is reflected in the metadata:

```json
{
  "rule": {
    "name": "Jigsaw Sudoku",
    "description": "Irregular regions instead of standard 3x3 boxes",
    "use_standard_boxes": false,
    "jigsaw_regions": [
      // ... region definitions
    ]
  }
}
```

This helps visualization tools understand how to render the puzzle.

## Adding Region Metadata

Rules with special regions/lines/areas should include them in metadata for visualization:

### Examples

**Jigsaw Sudoku**:
```python
def get_metadata(self):
    metadata = super().get_metadata()
    metadata['jigsaw_regions'] = self.jigsaw_regions
    metadata['use_standard_boxes'] = self.use_standard_boxes
    return metadata
```

**Windoku**:
```python
def get_metadata(self):
    metadata = super().get_metadata()
    metadata['windoku_regions'] = [
        [(r, c) for r in range(wr, wr + 3) for c in range(wc, wc + 3)]
        for wr, wc in self.windoku_windows
    ]
    return metadata
```

**Thermo**:
```python
def get_metadata(self):
    metadata = super().get_metadata()
    metadata['thermometers'] = self.thermometers
    return metadata
```

**Arrow**:
```python
def get_metadata(self):
    metadata = super().get_metadata()
    metadata['arrows'] = [
        {'circle': circle, 'arrow_cells': arrow_cells}
        for circle, arrow_cells in self.arrows
    ]
    return metadata
```

**Killer**:
```python
def get_metadata(self):
    metadata = super().get_metadata()
    metadata['cages'] = [
        {'sum': target_sum, 'cells': cells}
        for target_sum, cells in self.cages
    ]
    return metadata
```

## Implementation Checklist

When creating a new rule variant:

1. **Does it replace standard boxes?**
   - ☐ Yes → Set `self.use_standard_boxes = False`
   - ☑ No → Keep default `True`

2. **Does it have visual regions/lines/areas?**
   - ☑ Yes → Add them to `get_metadata()`
   - ☐ No → Use default metadata

3. **Test the rule**
   - ☐ Generate a puzzle
   - ☐ Verify metadata includes all visual elements
   - ☐ Check that constraints are enforced correctly

## Testing

Test Jigsaw without standard boxes:
```bash
python run.py sudoku_jigsaw_rule
```

Verify in metadata.json:
```bash
cat sudoku_jigsaw_rule/metadata.json | grep use_standard_boxes
# Should show: "use_standard_boxes": false
```

## Benefits

✅ **Correctness** - Rules now enforce only their intended constraints  
✅ **Flexibility** - Framework supports both standard and custom region types  
✅ **Visualization** - Metadata includes region information for rendering  
✅ **Clarity** - Explicit flag makes rule behavior clear  

## Migration Guide

Existing rules don't need changes unless they should disable standard boxes.

To migrate a rule that replaces boxes:

```python
# Before
class MyRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.custom_regions = [...]

# After
class MyRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.use_standard_boxes = False  # ← Add this
        self.custom_regions = [...]
    
    def get_metadata(self):  # ← Add this
        metadata = super().get_metadata()
        metadata['custom_regions'] = self.custom_regions
        return metadata
```

## Conclusion

The `use_standard_boxes` flag enables true regional variants in the Sudoku generator framework. Combined with metadata export of regions, this provides a complete solution for both generation and visualization of non-standard Sudoku variants.

