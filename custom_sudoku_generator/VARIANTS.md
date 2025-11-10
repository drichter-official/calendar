# Sudoku Variants - Complete List

This repository now contains **24 unique Sudoku variants** with their corresponding metadata, solutions, and puzzles.

## Complete List of Sudoku Variants

### 1. **Classic Sudoku** (Built-in)
Standard 9×9 Sudoku with rows, columns, and 3×3 boxes.

### 2. **Diagonal Sudoku (Sudoku X)** 
`sudoku_diagonal_rule/`
- Main diagonals must contain each digit 1-9 exactly once

### 3. **Anti-Knight Move**
`sudoku_knights_rule/`
- No two cells a chess knight's move apart can contain the same digit

### 4. **Anti-King Move**
`sudoku_kings_rule/`
- No adjacent cells (including diagonals) can have the same digit

### 5. **Windoku**
`sudoku_windoku_rule/`
- Four extra 3×3 regions must contain digits 1-9

### 6. **Killer Sudoku**
`sudoku_killer_rule/`
- Groups of cells (cages) must sum to specific values with no repeated digits

### 7. **Thermo Sudoku**
`sudoku_thermo_rule/`
- Digits strictly increase along thermometer lines

### 8. **Arrow Sudoku**
`sudoku_arrow_rule/`
- Sum of arrow cells must equal the circle cell value

### 9. **Skyscraper Sudoku**
`sudoku_skyscraper_rule/`
- Visibility clues around edges indicate visible buildings

### 10. **Consecutive Sudoku**
`sudoku_consecutive_rule/`
- Orthogonally adjacent cells may contain consecutive digits

### 11. **Nonconsecutive Sudoku**
`sudoku_nonconsecutive_rule/`
- Orthogonally adjacent cells cannot have consecutive digits

### 12. **Even-Odd Sudoku**
`sudoku_even_odd_rule/`
- Specific cells must contain even or odd digits

### 13. **Jigsaw Sudoku**
`sudoku_jigsaw_rule/`
- Irregular regions instead of standard 3×3 boxes

### 14. **Argyle**
`sudoku_argyle_rule/`
- Diagonals of 3×3 boxes must not contain repeated digits

### 15. **Asterisk**
`sudoku_asterisk_rule/`
- Nine cells forming an asterisk must contain digits 1-9

### 16. **Center Dot**
`sudoku_center_dot_rule/`
- Center cells of all 3×3 boxes must contain unique digits

### 17. **Futoshiki/Inequality Sudoku**
`sudoku_futoshiki_rule/`
- Inequality constraints between adjacent cells

### 18. **XV Sudoku**
`sudoku_xv_rule/`
- Specific adjacent cells must sum to 10 (X) or 5 (V)

### 19. **Kropki Sudoku**
`sudoku_kropki_rule/`
- Adjacent cells have specific difference or ratio relationships

### 20. **Chain Sudoku**
`sudoku_chain_rule/`
- Multiple overlapping grid constraints

### 21. **Sandwich Sudoku**
`sudoku_sandwich_rule/`
- Sum of digits between 1 and 9 in rows/columns follows constraints

### 22. **Renban Lines**
`sudoku_renban_rule/`
- Specific lines must contain consecutive digits in any order

### 23. **Whisper Lines**
`sudoku_whisper_rule/`
- Adjacent cells along whisper lines differ by at least 5

### 24. **Magic Square Region**
`sudoku_magic_square_rule/`
- Center 3×3 box must form a magic square

### 25. **Star Sudoku**
`sudoku_star_rule/`
- Cells in star pattern must contain unique digits

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
