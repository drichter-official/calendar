#!/usr/bin/env python
"""Test script to verify the even-odd rule with multiple patterns works correctly."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'custom_sudoku_generator'))

from sudoku_even_odd_rule.rule import EvenOddRule, PATTERNS, create_rule
from run import SudokuGenerator


def test_all_patterns_exist():
    """Test that all expected patterns are defined."""
    expected_patterns = ["checkerboard", "diamond", "cross", "corners", "stripes", "spiral"]
    for pattern in expected_patterns:
        assert pattern in PATTERNS, f"Pattern '{pattern}' not found in PATTERNS"
    print("✓ All expected patterns exist")


def test_pattern_structure():
    """Test that each pattern has the required structure."""
    for name, pattern in PATTERNS.items():
        assert 'name' in pattern, f"Pattern '{name}' missing 'name' field"
        assert 'description' in pattern, f"Pattern '{name}' missing 'description' field"
        assert 'even_cells' in pattern, f"Pattern '{name}' missing 'even_cells' field"
        assert 'odd_cells' in pattern, f"Pattern '{name}' missing 'odd_cells' field"
        assert isinstance(pattern['even_cells'], set), f"Pattern '{name}' even_cells should be a set"
        assert isinstance(pattern['odd_cells'], set), f"Pattern '{name}' odd_cells should be a set"
    print("✓ All patterns have correct structure")


def test_pattern_cells_valid():
    """Test that all cells are valid (0-8 range for 9x9 grid)."""
    for name, pattern in PATTERNS.items():
        for cell in pattern['even_cells']:
            assert len(cell) == 2, f"Pattern '{name}' has invalid cell tuple: {cell}"
            assert 0 <= cell[0] <= 8, f"Pattern '{name}' has invalid row: {cell}"
            assert 0 <= cell[1] <= 8, f"Pattern '{name}' has invalid col: {cell}"
        for cell in pattern['odd_cells']:
            assert len(cell) == 2, f"Pattern '{name}' has invalid cell tuple: {cell}"
            assert 0 <= cell[0] <= 8, f"Pattern '{name}' has invalid row: {cell}"
            assert 0 <= cell[1] <= 8, f"Pattern '{name}' has invalid col: {cell}"
    print("✓ All pattern cells are valid")


def test_no_overlap():
    """Test that even and odd cells don't overlap in any pattern."""
    for name, pattern in PATTERNS.items():
        overlap = pattern['even_cells'] & pattern['odd_cells']
        assert len(overlap) == 0, f"Pattern '{name}' has overlapping cells: {overlap}"
    print("✓ No overlapping even/odd cells in any pattern")


def test_rule_initialization():
    """Test that EvenOddRule initializes correctly with each pattern."""
    for pattern_name in PATTERNS:
        rule = EvenOddRule(pattern_name=pattern_name)
        assert rule.pattern_name == pattern_name
        assert pattern_name in rule.name or PATTERNS[pattern_name]['name'] in rule.name
        assert rule.even_cells == PATTERNS[pattern_name]['even_cells']
        assert rule.odd_cells == PATTERNS[pattern_name]['odd_cells']
    print("✓ EvenOddRule initializes correctly with each pattern")


def test_random_pattern_selection():
    """Test that patterns are randomly selected when no pattern_name is specified."""
    import random
    random.seed(42)
    
    patterns_seen = set()
    for _ in range(100):
        rule = EvenOddRule()
        patterns_seen.add(rule.pattern_name)
    
    # Should see multiple different patterns
    assert len(patterns_seen) > 1, "Random pattern selection doesn't seem to work"
    print(f"✓ Random pattern selection works (saw {len(patterns_seen)} different patterns)")


def test_validation():
    """Test that validation works correctly."""
    for pattern_name in PATTERNS:
        rule = EvenOddRule(pattern_name=pattern_name)
        grid = [[0] * 9 for _ in range(9)]
        
        # Test even cells require even numbers
        for cell in rule.even_cells:
            row, col = cell
            assert rule.validate(grid, row, col, 2) == True
            assert rule.validate(grid, row, col, 4) == True
            assert rule.validate(grid, row, col, 6) == True
            assert rule.validate(grid, row, col, 8) == True
            assert rule.validate(grid, row, col, 1) == False
            assert rule.validate(grid, row, col, 3) == False
            assert rule.validate(grid, row, col, 5) == False
            assert rule.validate(grid, row, col, 7) == False
            assert rule.validate(grid, row, col, 9) == False
        
        # Test odd cells require odd numbers
        for cell in rule.odd_cells:
            row, col = cell
            assert rule.validate(grid, row, col, 1) == True
            assert rule.validate(grid, row, col, 3) == True
            assert rule.validate(grid, row, col, 5) == True
            assert rule.validate(grid, row, col, 7) == True
            assert rule.validate(grid, row, col, 9) == True
            assert rule.validate(grid, row, col, 2) == False
            assert rule.validate(grid, row, col, 4) == False
            assert rule.validate(grid, row, col, 6) == False
            assert rule.validate(grid, row, col, 8) == False
    
    print("✓ Validation works correctly for all patterns")


def test_metadata():
    """Test that metadata includes pattern information."""
    for pattern_name in PATTERNS:
        rule = EvenOddRule(pattern_name=pattern_name)
        metadata = rule.get_metadata()
        
        assert 'pattern_name' in metadata
        assert metadata['pattern_name'] == pattern_name
        assert 'even_cells' in metadata
        assert 'odd_cells' in metadata
    
    print("✓ Metadata includes pattern information")


def test_create_rule_factory():
    """Test the create_rule factory function."""
    # Test without pattern_name (random selection)
    rule = create_rule()
    assert isinstance(rule, EvenOddRule)
    assert rule.pattern_name in PATTERNS
    
    # Test with specific pattern_name
    for pattern_name in PATTERNS:
        rule = create_rule(pattern_name=pattern_name)
        assert isinstance(rule, EvenOddRule)
        assert rule.pattern_name == pattern_name
    
    print("✓ create_rule factory function works")


if __name__ == '__main__':
    test_all_patterns_exist()
    test_pattern_structure()
    test_pattern_cells_valid()
    test_no_overlap()
    test_rule_initialization()
    test_random_pattern_selection()
    test_validation()
    test_metadata()
    test_create_rule_factory()
    print("\n✓✓✓ All tests passed! ✓✓✓")
