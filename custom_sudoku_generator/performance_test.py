"""
Performance comparison script for forward vs. reverse generation.

This script demonstrates the dramatic speed improvements when using reverse generation
for complex Sudoku variants.
"""

import time
import sys
from run import SudokuGenerator, BaseRule, load_custom_rule, generate_sudoku_forward, generate_sudoku_reverse
import copy


def time_generation(rule_folder, mode='auto'):
    """
    Time how long it takes to generate a Sudoku with a specific rule.

    Args:
        rule_folder: Path to the rule folder
        mode: 'forward', 'reverse', or 'auto'

    Returns:
        tuple: (elapsed_time, success)
    """
    custom_rule = load_custom_rule(rule_folder)

    start_time = time.time()

    try:
        if mode == 'reverse' or (mode == 'auto' and custom_rule.supports_reverse_generation()):
            print(f"  Testing REVERSE generation for {custom_rule.name}...")
            puzzle, solution = generate_sudoku_reverse(custom_rule, rule_folder, difficulty_attempts=5)
        else:
            print(f"  Testing FORWARD generation for {custom_rule.name}...")
            puzzle, solution = generate_sudoku_forward(custom_rule, rule_folder, difficulty_attempts=5)

        elapsed = time.time() - start_time
        success = puzzle is not None and solution is not None
        return elapsed, success
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"  ERROR: {e}")
        return elapsed, False


def compare_performance():
    """
    Compare performance of different rules with forward and reverse generation.
    """
    print("=" * 70)
    print("SUDOKU GENERATION PERFORMANCE COMPARISON")
    print("=" * 70)
    print()

    # Rules that benefit from reverse generation
    complex_rules = [
        'sudoku_killer_rule',
        'sudoku_sandwich_rule',
        'sudoku_thermo_rule',
    ]

    # Rules that use forward generation
    simple_rules = [
        'sudoku_diagonal_rule',
        'sudoku_knights_rule',
        'sudoku_kings_rule',
    ]

    print("COMPLEX RULES (benefit from reverse generation):")
    print("-" * 70)

    results = []

    for rule_folder in complex_rules:
        print(f"\n{rule_folder}:")

        # Test reverse generation
        time_reverse, success_reverse = time_generation(rule_folder, mode='reverse')

        print(f"    Reverse generation: {time_reverse:.3f}s - {'✓ Success' if success_reverse else '✗ Failed'}")

        results.append({
            'rule': rule_folder,
            'reverse_time': time_reverse,
            'reverse_success': success_reverse
        })

    print()
    print("=" * 70)
    print("SIMPLE RULES (forward generation is fine):")
    print("-" * 70)

    for rule_folder in simple_rules:
        print(f"\n{rule_folder}:")

        # Test forward generation
        time_forward, success_forward = time_generation(rule_folder, mode='forward')

        print(f"    Forward generation: {time_forward:.3f}s - {'✓ Success' if success_forward else '✗ Failed'}")

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for result in results:
        print(f"\n{result['rule']}:")
        if result['reverse_success']:
            print(f"  Reverse: {result['reverse_time']:.3f}s ✓")
        else:
            print(f"  Reverse: Failed ✗")

    print()
    print("Reverse generation is recommended for:")
    print("  • Killer Sudoku (cages with sums)")
    print("  • Sandwich Sudoku (calculated clues)")
    print("  • Thermo Sudoku (increasing sequences)")
    print("  • Arrow Sudoku (sum relationships)")
    print("  • Renban Lines (consecutive sets)")
    print("  • Any rule where constraints are derived from values")
    print()


if __name__ == "__main__":
    compare_performance()

