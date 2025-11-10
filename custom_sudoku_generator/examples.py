#!/usr/bin/env python3
"""
Example script demonstrating how to use the modular Sudoku generator programmatically.
"""

from run import SudokuGenerator, load_custom_rule, discover_rules
import os

def example_1_basic_sudoku():
    """Generate a basic Sudoku without custom rules."""
    print("=" * 60)
    print("Example 1: Basic Sudoku (no custom rules)")
    print("=" * 60)

    gen = SudokuGenerator()
    solution = gen.generate_full_grid()
    puzzle = gen.remove_numbers(attempts=5)

    print("\nSolution:")
    for row in solution:
        print(row)

    print("\nPuzzle:")
    for row in puzzle:
        print(row)
    print()


def example_2_with_custom_rule():
    """Generate a Sudoku with a custom rule loaded from a folder."""
    print("=" * 60)
    print("Example 2: Sudoku with Knight's Rule")
    print("=" * 60)

    # Load the custom rule
    custom_rule = load_custom_rule("sudoku_knights_rule")
    print(f"\nLoaded rule: {custom_rule.name}")
    print(f"Description: {custom_rule.description}")

    # Create generator with the rule
    gen = SudokuGenerator(custom_rule=custom_rule)
    solution = gen.generate_full_grid()
    puzzle = gen.remove_numbers(attempts=5)

    print("\nSolution:")
    for row in solution:
        print(row)

    print("\nPuzzle:")
    for row in puzzle:
        print(row)
    print()


def example_3_discover_and_generate():
    """Discover all available rules and generate a puzzle for each."""
    print("=" * 60)
    print("Example 3: Discover and generate for all rules")
    print("=" * 60)

    rule_folders = discover_rules()
    print(f"\nFound {len(rule_folders)} rule(s):")

    for folder in rule_folders:
        rule_name = os.path.basename(folder)
        print(f"\n  - {rule_name}")

    print("\nYou can generate puzzles for all rules using:")
    print("  python run.py --all")
    print()


def example_4_save_puzzle():
    """Generate and save a puzzle to a custom location."""
    print("=" * 60)
    print("Example 4: Generate and save to custom location")
    print("=" * 60)

    custom_rule = load_custom_rule("sudoku_knights_rule")
    gen = SudokuGenerator(custom_rule=custom_rule)

    solution = gen.generate_full_grid()
    puzzle = gen.remove_numbers(attempts=5)

    # Save to a custom output folder
    output_folder = "output_example"
    gen.save_puzzle(output_folder, puzzle, solution)
    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num == "1":
            example_1_basic_sudoku()
        elif example_num == "2":
            example_2_with_custom_rule()
        elif example_num == "3":
            example_3_discover_and_generate()
        elif example_num == "4":
            example_4_save_puzzle()
        else:
            print(f"Unknown example: {example_num}")
            print("Usage: python examples.py [1|2|3|4]")
    else:
        print("Modular Sudoku Generator - Examples\n")
        print("Run individual examples:")
        print("  python examples.py 1  - Basic Sudoku")
        print("  python examples.py 2  - Sudoku with Knight's Rule")
        print("  python examples.py 3  - Discover all available rules")
        print("  python examples.py 4  - Save puzzle to custom location")
        print("\nOr run all examples:")
        example_1_basic_sudoku()
        example_2_with_custom_rule()
        example_3_discover_and_generate()
        example_4_save_puzzle()

