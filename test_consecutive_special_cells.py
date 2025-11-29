#!/usr/bin/env python
"""Test script to verify that consecutive rule special cells are in the priority removal list."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'custom_sudoku_generator'))


def test_special_cells_exist():
    """Test that ConsecutiveRule has special_cells attribute."""
    from sudoku_consecutive_rule.rule import ConsecutiveRule
    
    rule = ConsecutiveRule()
    
    print("Testing that ConsecutiveRule has special_cells attribute...")
    
    if hasattr(rule, 'special_cells'):
        print("✓ SUCCESS: special_cells attribute exists")
        return True
    else:
        print("✗ FAIL: special_cells attribute missing")
        return False


def test_special_cells_populated_after_derive():
    """Test that special_cells are populated after deriving constraints."""
    from sudoku_consecutive_rule.rule import ConsecutiveRule
    
    rule = ConsecutiveRule()
    
    # Mock solution grid with known consecutive sequences
    solution = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ]
    
    print("\nTesting that special_cells are populated after derive_constraints_from_solution...")
    
    result = rule.derive_constraints_from_solution(solution)
    
    if not result:
        print("✗ FAIL: derive_constraints_from_solution returned False")
        return False
    
    if len(rule.consecutive_lines) == 0:
        print("✗ FAIL: No consecutive lines were found")
        return False
    
    if len(rule.special_cells) == 0:
        print("✗ FAIL: special_cells is empty after derivation")
        return False
    
    # Verify that special_cells contains endpoints of lines
    # Each line with length >= 2 should contribute 2 endpoints (or 1 if start equals end)
    expected_count = 0
    for line in rule.consecutive_lines:
        if len(line) >= 2:
            expected_count += 1  # first cell
            if line[0] != line[-1]:
                expected_count += 1  # last cell if different
    
    actual_count = len(rule.special_cells)
    
    if actual_count == expected_count:
        print(f"✓ SUCCESS: special_cells has {actual_count} cells (expected based on line endpoints)")
        return True
    else:
        print(f"✗ FAIL: expected {expected_count} special cells but got {actual_count}")
        return False


def test_special_cells_in_priority_list():
    """Test that special_cells are included in priority removal list."""
    from sudoku_consecutive_rule.rule import ConsecutiveRule
    
    rule = ConsecutiveRule()
    
    # Mock solution grid
    solution = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ]
    
    print("\nTesting that special_cells are in priority removal list...")
    
    rule.derive_constraints_from_solution(solution)
    priority_cells = rule.get_priority_removal_cells()
    
    missing_cells = []
    for cell in rule.special_cells:
        if cell not in priority_cells:
            missing_cells.append(cell)
    
    if len(missing_cells) == 0:
        print("✓ SUCCESS: All special cells are in priority removal list")
        return True
    else:
        print(f"✗ FAIL: {len(missing_cells)} special cells missing from priority list: {missing_cells}")
        return False


def test_special_cells_prioritized_first():
    """Test that special_cells appear first in the priority removal list."""
    from sudoku_consecutive_rule.rule import ConsecutiveRule
    
    rule = ConsecutiveRule()
    
    # Mock solution grid
    solution = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ]
    
    print("\nTesting that special_cells appear at the start of priority removal list...")
    
    rule.derive_constraints_from_solution(solution)
    priority_cells = rule.get_priority_removal_cells()
    
    # The first cells in priority_cells should be the special_cells
    # (in the order they appear in special_cells)
    special_count = len(rule.special_cells)
    first_priority = priority_cells[:special_count]
    
    # Check that all special cells are in the first positions
    all_special_first = all(cell in rule.special_cells for cell in first_priority)
    
    if all_special_first:
        print(f"✓ SUCCESS: First {special_count} priority cells are special cells")
        return True
    else:
        print(f"✗ FAIL: Special cells are not at the start of priority list")
        return False


def test_special_cells_in_metadata():
    """Test that special_cells are included in metadata."""
    from sudoku_consecutive_rule.rule import ConsecutiveRule
    
    rule = ConsecutiveRule()
    
    # Mock solution grid
    solution = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ]
    
    print("\nTesting that special_cells are in metadata...")
    
    rule.derive_constraints_from_solution(solution)
    metadata = rule.get_metadata()
    
    if 'special_cells' in metadata:
        if metadata['special_cells'] == rule.special_cells:
            print("✓ SUCCESS: special_cells are correctly included in metadata")
            return True
        else:
            print("✗ FAIL: special_cells in metadata don't match rule.special_cells")
            return False
    else:
        print("✗ FAIL: special_cells missing from metadata")
        return False


if __name__ == '__main__':
    results = []
    results.append(test_special_cells_exist())
    results.append(test_special_cells_populated_after_derive())
    results.append(test_special_cells_in_priority_list())
    results.append(test_special_cells_prioritized_first())
    results.append(test_special_cells_in_metadata())
    
    if all(results):
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n✗ {results.count(False)} test(s) failed!")
        sys.exit(1)
