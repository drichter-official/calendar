# Sudoku Generation Timeout Configuration

## Default Settings
- **Server Timeout**: 60 seconds (gunicorn)
- **Hard Mode**: 5 attempts × 10s timeout each (50s total max)
- **Medium Mode**: 10 attempts × 2s timeout each (20s total max)
- **Easy Mode**: 10 attempts × 1s timeout each (10s total max)

## Difficulty Level Settings

| Difficulty | Attempts | Timeout per Attempt | Removal Target |
|------------|----------|---------------------|----------------|
| Easy       | 10       | 1s                  | 50%            |
| Medium     | 10       | 2s                  | 66%            |
| Hard       | 5        | 10s                 | 90%            |

## How to Modify Timeout Duration

If you need to adjust the timeout duration, you can modify it in `run.py`:

### Option 1: Change the default timeout constants
In the top of `run.py`:
```python
# Hard: 5 attempts x 10s timeout each
HARD_ATTEMPT_COUNT = 5
HARD_ATTEMPT_TIMEOUT = 10
HARD_REMOVAL_TARGET = 0.90

# Medium: 10 attempts x 2s timeout each
MEDIUM_ATTEMPT_COUNT = 10
MEDIUM_ATTEMPT_TIMEOUT = 2
MEDIUM_REMOVAL_TARGET = 0.66

# Easy: 10 attempts x 1s timeout each
EASY_ATTEMPT_COUNT = 10
EASY_ATTEMPT_TIMEOUT = 1
EASY_REMOVAL_TARGET = 0.50
```

### Option 2: Set timeout per generation
In the `SudokuGenerator.__init__()` method:
```python
gen = SudokuGenerator(custom_rule=custom_rule)
gen.timeout_duration = 60  # Set to 60 seconds for this specific generation
```

## Timeout Behavior by Difficulty Level

Each difficulty level uses a multi-attempt approach:
- **Easy**: 10 attempts × 1s, stops after ~50% cells removed
- **Medium**: 10 attempts × 2s, stops after ~66% cells removed
- **Hard**: 5 attempts × 10s, continues until ~90% cells removed

The best attempt (with the most cells removed) is selected as the final puzzle.

## When Timeout Occurs

1. A message is printed: `⏱️ Timeout reached (Xs). Saving best puzzle found so far...`
2. The current attempt ends and the next attempt begins
3. After all attempts, the puzzle with the most cells removed is selected
4. The complete solution grid is saved alongside the puzzle

## No Timeout Needed?

If you want to disable the timeout entirely:
```python
gen.timeout_duration = float('inf')  # Never timeout
```

Or set it to 0 to skip timeout checks:
```python
gen.timeout_duration = 0  # Disabled
```

