#!/usr/bin/env python3
"""
Test script to verify the timeout functionality works correctly.
"""

import sys
import os

# Add the custom_sudoku_generator directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_sudoku_generator'))

from run import SudokuGenerator
from base_rule import BaseRule
import time

def test_timeout():
    print("Testing timeout functionality...")
    print("Creating a generator with 5 second timeout...")

    gen = SudokuGenerator(custom_rule=BaseRule())
    gen.timeout_duration = 5  # Set a short timeout for testing

    print("Generating full solution...")
    gen.generate_full_grid()

    print("Attempting to remove numbers (this will timeout after 5 seconds)...")
    start = time.time()
    puzzle = gen.remove_numbers(attempts=50, difficulty='hard')  # High attempts to trigger timeout
    elapsed = time.time() - start

    print(f"\n✅ Process completed in {elapsed:.2f} seconds")

    if gen.timed_out:
        print("✅ Timeout was triggered successfully!")
    else:
        print("⚠️  Timeout was not triggered (generation completed quickly)")

    # Count the number of empty cells
    empty_cells = sum(row.count(0) for row in puzzle)
    print(f"✅ Puzzle has {empty_cells} empty cells")
    print("\nPuzzle state:")
    for row in puzzle[:3]:  # Show first 3 rows
        print(row)
    print("...")

if __name__ == "__main__":
    test_timeout()

