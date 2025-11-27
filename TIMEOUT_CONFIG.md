# Sudoku Generation Timeout Configuration

## Default Settings
- **Timeout Duration**: 30 seconds
- **Behavior**: Saves the best puzzle found before timeout

## How to Modify Timeout Duration

If you need to adjust the timeout duration, you can modify it in `run.py`:

### Option 1: Change the default timeout
In the `SudokuGenerator.__init__()` method (around line 16):
```python
self.timeout_duration = 30  # Change this value (in seconds)
```

### Option 2: Set timeout per generation
In the `generate_sudoku_forward()` or `generate_sudoku_reverse()` functions:
```python
gen = SudokuGenerator(custom_rule=custom_rule)
gen.timeout_duration = 60  # Set to 60 seconds for this specific generation
```

## Timeout Behavior by Difficulty Level

The timeout applies to all difficulty levels:
- **Easy**: Stops after ~50% cells removed OR timeout reached
- **Medium**: Stops after ~75% cells removed OR timeout reached  
- **Hard**: Continues until no more cells can be removed OR timeout reached

## When Timeout Occurs

1. A message is printed: `⏱️ Timeout reached (30s). Saving best puzzle found so far...`
2. The current puzzle state (with cells removed so far) is saved
3. The complete solution grid is saved
4. Metadata is saved with generation information

## No Timeout Needed?

If you want to disable the timeout entirely:
```python
gen.timeout_duration = float('inf')  # Never timeout
```

Or set it to 0 to skip timeout checks:
```python
gen.timeout_duration = 0  # Disabled
```

