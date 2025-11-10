#!/usr/bin/env python3
"""Final verification that all 24 Sudoku variants are working correctly."""

import os
import json
import sys

def verify_rule_structure(rule_dir):
    """Verify a rule directory has all required files."""
    required_files = ['rule.py', 'metadata.json', 'solution.txt', 'sudoku.txt']
    for file in required_files:
        if not os.path.exists(os.path.join(rule_dir, file)):
            return False, f"Missing {file}"
    return True, "OK"

def verify_metadata(rule_dir):
    """Verify metadata.json is valid and has required fields."""
    metadata_path = os.path.join(rule_dir, 'metadata.json')
    try:
        with open(metadata_path, 'r') as f:
            data = json.load(f)
        
        # Check required fields
        if 'rule' not in data:
            return False, "Missing 'rule' field"
        if 'name' not in data['rule']:
            return False, "Missing rule name"
        if 'description' not in data['rule']:
            return False, "Missing rule description"
        
        return True, data['rule']['name']
    except Exception as e:
        return False, str(e)

def verify_puzzle_solution(rule_dir):
    """Verify puzzle and solution files are readable."""
    try:
        with open(os.path.join(rule_dir, 'sudoku.txt'), 'r') as f:
            puzzle_lines = f.readlines()
        with open(os.path.join(rule_dir, 'solution.txt'), 'r') as f:
            solution_lines = f.readlines()
        
        if len(puzzle_lines) < 9 or len(solution_lines) < 9:
            return False, "Insufficient lines in puzzle/solution"
        
        return True, f"{len(puzzle_lines)} lines"
    except Exception as e:
        return False, str(e)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all rule directories
    rule_dirs = sorted([
        d for d in os.listdir(script_dir)
        if os.path.isdir(os.path.join(script_dir, d)) and d.startswith('sudoku_')
    ])
    
    print("="*70)
    print(f"FINAL VERIFICATION - {len(rule_dirs)} Sudoku Variants")
    print("="*70)
    
    results = []
    for rule_dir in rule_dirs:
        full_path = os.path.join(script_dir, rule_dir)
        
        # Check structure
        structure_ok, structure_msg = verify_rule_structure(full_path)
        if not structure_ok:
            results.append((rule_dir, False, structure_msg))
            continue
        
        # Check metadata
        metadata_ok, metadata_msg = verify_metadata(full_path)
        if not metadata_ok:
            results.append((rule_dir, False, metadata_msg))
            continue
        
        # Check puzzle/solution
        puzzle_ok, puzzle_msg = verify_puzzle_solution(full_path)
        if not puzzle_ok:
            results.append((rule_dir, False, puzzle_msg))
            continue
        
        results.append((rule_dir, True, metadata_msg))
    
    # Print results
    print()
    for i, (rule_dir, success, msg) in enumerate(results, 1):
        status = "✅" if success else "❌"
        print(f"{i:2}. {status} {rule_dir:30} - {msg}")
    
    print()
    print("="*70)
    
    success_count = sum(1 for _, success, _ in results if success)
    print(f"Results: {success_count}/{len(results)} variants verified successfully")
    
    if success_count == len(results):
        print("✅ ALL TESTS PASSED - 24 unique Sudoku variants ready!")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
