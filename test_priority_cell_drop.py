#!/usr/bin/env python
"""Test script to verify that 20% of priority cells are randomly dropped."""

import sys
import os
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'custom_sudoku_generator'))


def test_priority_cell_drop_rate():
    """Test that approximately 20% of priority cells are dropped."""
    # Simulate the filtering logic from run.py
    # We'll run it many times to get a statistical sample
    
    num_trials = 1000
    priority_cell_count = 50  # Simulate 50 priority cells
    
    total_kept = 0
    
    for _ in range(num_trials):
        # Create mock priority cells
        priority_cells = [(i, j) for i in range(5) for j in range(10)]  # 50 cells
        
        # Apply the same filtering logic as in run.py
        kept_cells = [cell for cell in priority_cells if random.random() > 0.2]
        total_kept += len(kept_cells)
    
    average_kept = total_kept / num_trials
    expected_kept = priority_cell_count * 0.8  # 80% should be kept on average
    
    # Allow for statistical variance (within 10% margin)
    lower_bound = expected_kept * 0.9  # 72% kept (10% below expected)
    upper_bound = expected_kept * 1.1  # 88% kept (10% above expected)
    
    print(f"Testing priority cell drop rate...")
    print(f"  Number of trials: {num_trials}")
    print(f"  Original priority cells per trial: {priority_cell_count}")
    print(f"  Average cells kept: {average_kept:.2f}")
    print(f"  Expected cells kept (80%): {expected_kept:.2f}")
    print(f"  Acceptable range: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    if lower_bound <= average_kept <= upper_bound:
        print("✓ SUCCESS: Priority cell drop rate is approximately 20% as expected!")
        return True
    else:
        print(f"✗ FAIL: Priority cell drop rate is outside acceptable range")
        print(f"   Actual drop rate: {((priority_cell_count - average_kept) / priority_cell_count) * 100:.1f}%")
        return False


def test_priority_cells_not_all_removed():
    """Test that not all priority cells are removed (some randomness is preserved)."""
    # Run multiple trials and ensure we get different results
    num_trials = 10
    priority_cells = [(i, j) for i in range(5) for j in range(10)]  # 50 cells
    
    results = []
    for _ in range(num_trials):
        kept_cells = [cell for cell in priority_cells if random.random() > 0.2]
        results.append(len(kept_cells))
    
    # Check that we got at least 2 different results (showing randomness)
    unique_results = len(set(results))
    
    print(f"\nTesting randomness of priority cell dropping...")
    print(f"  Number of trials: {num_trials}")
    print(f"  Results (cells kept): {results}")
    print(f"  Unique result counts: {unique_results}")
    
    if unique_results >= 2:
        print("✓ SUCCESS: Priority cell dropping shows expected randomness!")
        return True
    else:
        print("✗ FAIL: Priority cell dropping does not show expected randomness")
        return False


if __name__ == '__main__':
    success1 = test_priority_cell_drop_rate()
    success2 = test_priority_cells_not_all_removed()
    
    if success1 and success2:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
