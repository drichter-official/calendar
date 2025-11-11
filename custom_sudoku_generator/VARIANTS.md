# Sudoku Variants - Complete List

This repository contains **25 unique Sudoku variants** with their corresponding metadata, solutions, and puzzles.

## Implementation Status

### ✅ Fully Implemented (Complex Constraint Rules)

These variants have proper, complete implementations with complex constraints:

### 1. **Classic Sudoku** (Built-in)
Standard 9×9 Sudoku with rows, columns, and 3×3 boxes.

### 2. **Diagonal Sudoku (Sudoku X)** ✅
`sudoku_diagonal_rule/`
- Main diagonals must contain each digit 1-9 exactly once
- Both diagonals fully enforced

### 3. **Anti-Knight Move** ✅
`sudoku_knights_rule/`
- No two cells a chess knight's move apart can contain the same digit
- All 8 knight move directions checked

### 4. **Anti-King Move** ✅
`sudoku_kings_rule/`
- No adjacent cells (including diagonals) can have the same digit
- All 8 surrounding cells checked

### 5. **Windoku** ✅
`sudoku_windoku_rule/`
- Four extra 3×3 regions must contain digits 1-9
- All four windoku windows at positions (1,1), (1,5), (5,1), (5,5)

### 6. **Killer Sudoku** ✅
`sudoku_killer_rule/`
- Groups of cells (cages) must sum to specific values with no repeated digits
- 10+ cages with varying sizes (2-4 cells) and target sums (8-23)

### 7. **Thermo Sudoku** ✅
`sudoku_thermo_rule/`
- Digits strictly increase along thermometer lines
- 5 thermometers: horizontal, vertical, and diagonal with varying lengths

### 8. **Arrow Sudoku** ✅
`sudoku_arrow_rule/`
- Sum of arrow cells must equal the circle cell value
- 5 arrows with varying lengths and directions (horizontal, vertical, diagonal)

### 9. **Nonconsecutive Sudoku** ✅
`sudoku_nonconsecutive_rule/`
- Orthogonally adjacent cells cannot have consecutive digits
- Applied globally across entire grid

### 10. **Even-Odd Sudoku** ✅
`sudoku_even_odd_rule/`
- Specific cells must contain even or odd digits
- 25 marked cells (13 even, 12 odd) distributed across grid

### 11. **Jigsaw Sudoku** ✅
`sudoku_jigsaw_rule/`
- Irregular regions instead of standard 3×3 boxes
- 9 truly irregular regions with non-standard shapes

### 12. **Argyle** ✅
`sudoku_argyle_rule/`
- Diagonals of 3×3 boxes must not contain repeated digits
- Both diagonals checked in all 9 boxes

### 13. **Asterisk** ✅
`sudoku_asterisk_rule/`
- Nine cells forming an asterisk must contain digits 1-9
- Asterisk centered at (4,4) with 8 arms

### 14. **Center Dot** ✅
`sudoku_center_dot_rule/`
- Center cells of all 3×3 boxes must contain unique digits
- All 9 center cells form additional constraint region

### 15. **Futoshiki/Inequality Sudoku** ✅
`sudoku_futoshiki_rule/`
- Inequality constraints between adjacent cells
- 10 inequality markers (< and >) across grid

### 16. **XV Sudoku** ✅
`sudoku_xv_rule/`
- Specific adjacent cells must sum to 10 (X) or 5 (V)
- 8 X markers (sum to 10) and 7 V markers (sum to 5)

### 17. **Kropki Sudoku** ✅
`sudoku_kropki_rule/`
- Adjacent cells have specific difference or ratio relationships
- 7 white dots (differ by 1) and 6 black dots (ratio 1:2)

### 18. **Consecutive Sudoku** ✅
`sudoku_consecutive_rule/`
- Marked cells must be consecutive, unmarked cells cannot be
- 9 white dot markers; negative constraint enforced elsewhere

### 19. **Sandwich Sudoku** ✅
`sudoku_sandwich_rule/`
- Sum of digits between 1 and 9 in rows/columns equals given clues
- 6 sandwich clues (3 rows, 3 columns) with sums 12-22

### 20. **Renban Lines** ✅
`sudoku_renban_rule/`
- Specific lines must contain consecutive digits in any order
- 6 renban lines of varying lengths (3-4 cells)

### 21. **Whisper Lines** ✅
`sudoku_whisper_rule/`
- Adjacent cells along whisper lines differ by at least 5
- 5 whisper lines (vertical, horizontal, L-shaped)

### 22. **Magic Square Region** ✅
`sudoku_magic_square_rule/`
- Center 3×3 box must form a magic square
- All rows, columns, and diagonals in center box sum to 15

### 23. **Star Sudoku** ✅
`sudoku_star_rule/`
- Cells in star pattern must contain unique digits
- 9 cells forming star at center with 8 directional points

### ⚠️ Simplified Implementations

These variants have basic implementations but could be enhanced:

### 24. **Chain Sudoku** ⚠️
`sudoku_chain_rule/`
- Multiple overlapping grid constraints
- Currently: Only top-left corners of boxes must be unique
- Enhancement needed: True overlapping grid structure

### 25. **Skyscraper Sudoku** ⚠️
`sudoku_skyscraper_rule/`
- Visibility clues around edges indicate visible buildings
- Currently: No actual validation (returns true always)
- Enhancement needed: Edge clues and visibility calculation

## File Structure

Each rule folder contains:
- `rule.py` - Rule implementation following the BaseRule pattern
- `sudoku.txt` - Generated puzzle with some cells empty (represented as 0)
- `solution.txt` - Complete solution grid
- `metadata.json` - Rule metadata including name, description, and generation timestamp

## Usage

### List All Available Rules
```bash
python run.py
```

### Generate for a Specific Rule
```bash
python run.py sudoku_diagonal_rule/ 5
```

### Generate All Rules at Once
```bash
python run.py --all
```

### Generate by Index
```bash
python run.py --index 5
```

### Generate All with Helper Script
```bash
python generate_all.py
```

## Implementation Notes

All rules follow the modular pattern established by the project:
1. Each rule inherits from `BaseRule`
2. Implements a `validate()` method for custom constraints
3. Includes a `create_rule()` factory function
4. Has descriptive name and description fields

Some rules have been simplified to balance constraint complexity with puzzle generation feasibility. The implementations focus on demonstrating the core concept of each variant while ensuring puzzles can be generated in reasonable time.
