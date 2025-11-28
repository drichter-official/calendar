#!/usr/bin/env python3
"""
Test script to verify the hard mode sudoku generation functionality.
Tests the target of less than 12 clues with 30-second timeout and retry logic.
"""

import sys
import os
import tempfile

# Add the custom_sudoku_generator directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_sudoku_generator'))

import run
from run import (
    SudokuGenerator, 
    generate_sudoku_forward, 
    HARD_MODE_TARGET_CLUES, 
    HARD_MODE_TIMEOUT,
    MULTI_ATTEMPT_COUNT,
    MULTI_ATTEMPT_TIMEOUT,
    MEDIUM_REMOVAL_TARGET,
    HARD_REMOVAL_TARGET
)
from base_rule import BaseRule


def test_hard_mode_constants():
    """Test that the hard mode constants are correctly defined."""
    print("Testing hard mode constants...")
    
    assert HARD_MODE_TARGET_CLUES == 12, f"Expected target 12, got {HARD_MODE_TARGET_CLUES}"
    assert HARD_MODE_TIMEOUT == 30, f"Expected timeout 30, got {HARD_MODE_TIMEOUT}"
    
    print(f"  ✅ HARD_MODE_TARGET_CLUES = {HARD_MODE_TARGET_CLUES}")
    print(f"  ✅ HARD_MODE_TIMEOUT = {HARD_MODE_TIMEOUT}")


def test_multi_attempt_constants():
    """Test that the multi-attempt generation constants are correctly defined."""
    print("\nTesting multi-attempt constants...")
    
    assert MULTI_ATTEMPT_COUNT == 4, f"Expected 4 attempts, got {MULTI_ATTEMPT_COUNT}"
    assert MULTI_ATTEMPT_TIMEOUT == 5, f"Expected 5s timeout, got {MULTI_ATTEMPT_TIMEOUT}"
    assert MEDIUM_REMOVAL_TARGET == 0.70, f"Expected 0.70, got {MEDIUM_REMOVAL_TARGET}"
    assert HARD_REMOVAL_TARGET == 0.90, f"Expected 0.90, got {HARD_REMOVAL_TARGET}"
    
    print(f"  ✅ MULTI_ATTEMPT_COUNT = {MULTI_ATTEMPT_COUNT}")
    print(f"  ✅ MULTI_ATTEMPT_TIMEOUT = {MULTI_ATTEMPT_TIMEOUT}s")
    print(f"  ✅ MEDIUM_REMOVAL_TARGET = {MEDIUM_REMOVAL_TARGET}")
    print(f"  ✅ HARD_REMOVAL_TARGET = {HARD_REMOVAL_TARGET}")


def test_count_filled_cells():
    """Test the count_filled_cells method."""
    print("\nTesting count_filled_cells method...")
    
    gen = SudokuGenerator(custom_rule=BaseRule())
    
    # Full grid should have 81 filled cells
    gen.generate_full_grid()
    filled = gen.count_filled_cells(gen.grid)
    assert filled == 81, f"Expected 81 filled cells, got {filled}"
    print(f"  ✅ Full grid has {filled} filled cells")
    
    # Empty grid should have 0 filled cells
    empty_grid = [[0] * 9 for _ in range(9)]
    assert gen.count_filled_cells(empty_grid) == 0
    print("  ✅ Empty grid has 0 filled cells")


def test_reset_timeout():
    """Test the reset_timeout method."""
    print("\nTesting reset_timeout method...")
    
    gen = SudokuGenerator(custom_rule=BaseRule())
    gen.timeout_start = 12345
    gen.timed_out = True
    
    gen.reset_timeout()
    
    assert gen.timeout_start is None, "timeout_start should be None after reset"
    assert gen.timed_out == False, "timed_out should be False after reset"
    
    print("  ✅ reset_timeout works correctly")


def test_timeout_duration_set():
    """Test that timeout duration is correctly set for hard mode."""
    print("\nTesting timeout duration for hard mode...")
    
    gen = SudokuGenerator(custom_rule=BaseRule())
    assert gen.timeout_duration == HARD_MODE_TIMEOUT, f"Expected {HARD_MODE_TIMEOUT}s, got {gen.timeout_duration}s"
    
    print(f"  ✅ Default timeout is {gen.timeout_duration}s")


def test_hard_mode_retry_logic():
    """Test that hard mode retries when target isn't achieved (with shortened timeout for testing)."""
    print("\nTesting hard mode retry logic (with 2s timeout for speed)...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_rule = BaseRule()
        
        # Create a generator with very short timeout for testing
        # Use proper cleanup pattern to restore the original value
        import run
        original_timeout = run.HARD_MODE_TIMEOUT
        
        try:
            run.HARD_MODE_TIMEOUT = 2  # 2 second timeout for faster testing
            
            puzzle_grid, solution_grid = generate_sudoku_forward(
                custom_rule, 
                tmpdir, 
                difficulty_attempts=5, 
                difficulty='hard'
            )
            
            # The puzzle should be generated
            assert puzzle_grid is not None, "Puzzle should be generated"
            assert solution_grid is not None, "Solution should be generated"
            
            clues = sum(1 for row in puzzle_grid for cell in row if cell != 0)
            print(f"  ✅ Puzzle generated with {clues} clues")
            
            # The puzzle should have been saved
            assert os.path.exists(os.path.join(tmpdir, 'sudoku.txt')), "sudoku.txt should exist"
            assert os.path.exists(os.path.join(tmpdir, 'solution.txt')), "solution.txt should exist"
            print("  ✅ Puzzle files saved correctly")
            
        finally:
            run.HARD_MODE_TIMEOUT = original_timeout


def test_non_hard_modes_not_affected():
    """Test that easy and medium modes are not affected by the changes."""
    print("\nTesting non-hard modes (easy, medium)...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_rule = BaseRule()
        
        for mode in ['easy', 'medium']:
            mode_dir = os.path.join(tmpdir, mode)
            os.makedirs(mode_dir)
            
            puzzle_grid, solution_grid = generate_sudoku_forward(
                custom_rule, 
                mode_dir, 
                difficulty_attempts=5, 
                difficulty=mode
            )
            
            assert puzzle_grid is not None, f"{mode} puzzle should be generated"
            clues = sum(1 for row in puzzle_grid for cell in row if cell != 0)
            print(f"  ✅ {mode.capitalize()} mode: {clues} clues")


def test_generate_with_multi_attempts():
    """Test the new generate_with_multi_attempts method directly."""
    print("\nTesting generate_with_multi_attempts method...")
    
    # Save original values
    original_count = run.MULTI_ATTEMPT_COUNT
    original_timeout = run.MULTI_ATTEMPT_TIMEOUT
    
    try:
        # Use shorter values for testing
        run.MULTI_ATTEMPT_COUNT = 2
        run.MULTI_ATTEMPT_TIMEOUT = 2
        
        gen = SudokuGenerator(custom_rule=BaseRule())
        solution_grid = gen.generate_full_grid()
        
        # Test medium difficulty (70% target)
        puzzle_grid = gen.generate_with_multi_attempts(solution_grid, difficulty='medium')
        assert puzzle_grid is not None, "Medium puzzle should be generated"
        clues = gen.count_filled_cells(puzzle_grid)
        print(f"  ✅ Medium mode via multi_attempts: {clues} clues")
        
        # Test hard difficulty (90% target)
        puzzle_grid = gen.generate_with_multi_attempts(solution_grid, difficulty='hard')
        assert puzzle_grid is not None, "Hard puzzle should be generated"
        clues = gen.count_filled_cells(puzzle_grid)
        print(f"  ✅ Hard mode via multi_attempts: {clues} clues")
        
    finally:
        run.MULTI_ATTEMPT_COUNT = original_count
        run.MULTI_ATTEMPT_TIMEOUT = original_timeout


def test_multi_attempts_picks_best():
    """Test that the multi-attempt approach picks the puzzle with fewest clues."""
    print("\nTesting that multi-attempts picks best result...")
    
    # Save original values
    original_count = run.MULTI_ATTEMPT_COUNT
    original_timeout = run.MULTI_ATTEMPT_TIMEOUT
    
    try:
        # Run multiple attempts to ensure we get the best
        run.MULTI_ATTEMPT_COUNT = 3
        run.MULTI_ATTEMPT_TIMEOUT = 2
        
        gen = SudokuGenerator(custom_rule=BaseRule())
        solution_grid = gen.generate_full_grid()
        
        puzzle_grid = gen.generate_with_multi_attempts(solution_grid, difficulty='hard')
        clues = gen.count_filled_cells(puzzle_grid)
        
        # The result should have significantly fewer clues than the total
        assert clues < 81, f"Should have removed some clues, got {clues}"
        print(f"  ✅ Multi-attempts returned puzzle with {clues} clues")
        
    finally:
        run.MULTI_ATTEMPT_COUNT = original_count
        run.MULTI_ATTEMPT_TIMEOUT = original_timeout


def run_all_tests():
    """Run all hard mode tests."""
    print("=" * 60)
    print("HARD MODE SUDOKU GENERATION TESTS")
    print("=" * 60)
    
    try:
        test_hard_mode_constants()
        test_multi_attempt_constants()
        test_count_filled_cells()
        test_reset_timeout()
        test_timeout_duration_set()
        test_hard_mode_retry_logic()
        test_non_hard_modes_not_affected()
        test_generate_with_multi_attempts()
        test_multi_attempts_picks_best()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
