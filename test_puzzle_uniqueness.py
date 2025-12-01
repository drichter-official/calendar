#!/usr/bin/env python
"""Test that all puzzles have exactly one solution."""

import sys
import os
import ast
import copy

# Add the custom_sudoku_generator directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_sudoku_generator'))

from run import SudokuGenerator, load_custom_rule, discover_rules
from base_rule import BaseRule


def test_puzzle_uniqueness():
    """Test that all puzzles have exactly one solution."""
    print("=" * 60)
    print("PUZZLE UNIQUENESS TEST")
    print("=" * 60)
    
    rule_folders = discover_rules()
    all_passed = True
    
    for rule_folder in rule_folders:
        rule_name = os.path.basename(rule_folder)
        puzzle_path = os.path.join(rule_folder, 'sudoku.txt')
        
        if not os.path.exists(puzzle_path):
            print(f"⚠️  {rule_name}: No puzzle file found")
            continue
        
        # Load the puzzle
        with open(puzzle_path, 'r') as f:
            puzzle = [ast.literal_eval(line.strip()) for line in f if line.strip()]
        
        # Load the custom rule
        custom_rule = load_custom_rule(rule_folder)
        
        # Create a generator with the custom rule
        gen = SudokuGenerator(custom_rule=custom_rule)
        gen.timeout_start = None
        gen.timed_out = False
        
        # Count solutions
        solutions = gen.count_solutions(copy.deepcopy(puzzle), 0)
        
        if solutions == 1:
            print(f"✅ {rule_name}: Unique solution")
        else:
            print(f"❌ {rule_name}: {solutions} solutions found!")
            all_passed = False
    
    print()
    print("=" * 60)
    if all_passed:
        print("✅ ALL PUZZLES HAVE UNIQUE SOLUTIONS")
    else:
        print("❌ SOME PUZZLES HAVE MULTIPLE SOLUTIONS")
    print("=" * 60)
    
    return all_passed


if __name__ == '__main__':
    success = test_puzzle_uniqueness()
    sys.exit(0 if success else 1)
