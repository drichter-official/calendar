"""
Performance test script for all Sudoku rules generation.

This script tests all available Sudoku rules, measures generation times,
calculates averages, and ranks them from fastest to slowest.

Usage:
    python performance_test.py                     # Interactive mode, prompts for number of iterations
    python performance_test.py 5                   # Run 5 iterations per rule
    python performance_test.py 3 --timeout 60      # Run 3 iterations per rule with 60s timeout
"""

import time
import sys
import os
import signal
from multiprocessing import Process, Queue
from run import load_custom_rule, generate_sudoku_forward, generate_sudoku_reverse, discover_rules


# Default timeout in seconds (2 minutes per iteration)
DEFAULT_TIMEOUT = 120


def _generation_worker(rule_folder, result_queue):
    """
    Worker function to run generation in a separate process.
    This allows us to implement a timeout.
    """
    try:
        custom_rule = load_custom_rule(rule_folder)
        start_time = time.time()
        
        if custom_rule.supports_reverse_generation():
            puzzle, solution = generate_sudoku_reverse(custom_rule, rule_folder, difficulty_attempts=5)
        else:
            puzzle, solution = generate_sudoku_forward(custom_rule, rule_folder, difficulty_attempts=5)
        
        elapsed = time.time() - start_time
        success = puzzle is not None and solution is not None
        result_queue.put((elapsed, success, None))
    except Exception as e:
        elapsed = time.time() - start_time if 'start_time' in locals() else 0
        result_queue.put((elapsed, False, str(e)))


def time_single_generation(rule_folder, timeout=DEFAULT_TIMEOUT, verbose=False):
    """
    Time how long it takes to generate a single Sudoku with a specific rule.

    Args:
        rule_folder: Path to the rule folder
        timeout: Maximum time allowed for generation in seconds
        verbose: Whether to print detailed output

    Returns:
        tuple: (elapsed_time, success, timed_out)
    """
    result_queue = Queue()
    process = Process(target=_generation_worker, args=(rule_folder, result_queue))
    
    start_time = time.time()
    process.start()
    process.join(timeout=timeout)
    
    if process.is_alive():
        # Process timed out
        process.terminate()
        process.join(timeout=5)
        if process.is_alive():
            process.kill()
            process.join()
        elapsed = time.time() - start_time
        if verbose:
            print(f"    TIMEOUT after {timeout}s")
        return elapsed, False, True
    
    # Get result from queue
    if not result_queue.empty():
        elapsed, success, error = result_queue.get()
        if error and verbose:
            print(f"    ERROR: {error}")
        return elapsed, success, False
    
    # No result - something went wrong
    elapsed = time.time() - start_time
    return elapsed, False, False


def run_performance_test(num_iterations=5, timeout=DEFAULT_TIMEOUT, verbose=False):
    """
    Run performance tests for all Sudoku rules.

    Args:
        num_iterations: Number of sudokus to generate per rule
        timeout: Maximum time allowed per generation in seconds
        verbose: Whether to print detailed output during generation
    """
    print("=" * 70)
    print("SUDOKU GENERATION PERFORMANCE TEST")
    print("=" * 70)
    print()

    # Discover all rule folders
    rule_folders = discover_rules()
    
    if not rule_folders:
        print("No rule folders found!")
        return

    print(f"Found {len(rule_folders)} rules to test")
    print(f"Generating {num_iterations} sudoku(s) per rule")
    print(f"Timeout per generation: {timeout}s")
    print("-" * 70)
    print()

    results = []

    for i, rule_folder in enumerate(rule_folders, 1):
        rule_name = os.path.basename(rule_folder)
        custom_rule = load_custom_rule(rule_folder)
        
        print(f"[{i}/{len(rule_folders)}] Testing: {rule_name}")
        print(f"         ({custom_rule.name})")
        
        times = []
        successes = 0
        timeouts = 0
        
        for iteration in range(num_iterations):
            elapsed, success, timed_out = time_single_generation(rule_folder, timeout=timeout, verbose=verbose)
            times.append(elapsed)
            
            if success:
                successes += 1
            if timed_out:
                timeouts += 1
            
            # Show progress
            if timed_out:
                status = "⏱ TIMEOUT"
            elif success:
                status = "✓"
            else:
                status = "✗"
            print(f"    Run {iteration + 1}: {elapsed:.3f}s {status}")
        
        # Calculate statistics
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        success_rate = (successes / num_iterations) * 100
        
        results.append({
            'rule_folder': rule_name,
            'rule_name': custom_rule.name,
            'avg_time': avg_time,
            'min_time': min_time,
            'max_time': max_time,
            'times': times,
            'successes': successes,
            'timeouts': timeouts,
            'total': num_iterations,
            'success_rate': success_rate
        })
        
        print(f"    Average: {avg_time:.3f}s (min: {min_time:.3f}s, max: {max_time:.3f}s)")
        print(f"    Success rate: {successes}/{num_iterations} ({success_rate:.0f}%)")
        if timeouts > 0:
            print(f"    Timeouts: {timeouts}/{num_iterations}")
        print()

    # Sort results by average time (fastest first)
    results.sort(key=lambda x: x['avg_time'])

    # Print ranked results
    print()
    print("=" * 70)
    print("PERFORMANCE RANKING (Fastest to Slowest)")
    print("=" * 70)
    print()
    print(f"{'Rank':<5} {'Rule':<40} {'Avg Time':<12} {'Success Rate':<12}")
    print("-" * 70)

    for rank, result in enumerate(results, 1):
        rule_display = result['rule_folder'][:38]
        avg_time_str = f"{result['avg_time']:.3f}s"
        success_str = f"{result['success_rate']:.0f}%"
        
        print(f"{rank:<5} {rule_display:<40} {avg_time_str:<12} {success_str:<12}")

    print()
    print("=" * 70)
    print("DETAILED STATISTICS")
    print("=" * 70)

    for rank, result in enumerate(results, 1):
        print(f"\n{rank}. {result['rule_folder']}")
        print(f"   Display Name: {result['rule_name']}")
        print(f"   Average Time: {result['avg_time']:.3f}s")
        print(f"   Min Time:     {result['min_time']:.3f}s")
        print(f"   Max Time:     {result['max_time']:.3f}s")
        print(f"   Success Rate: {result['successes']}/{result['total']} ({result['success_rate']:.0f}%)")
        print(f"   All Times:    {[f'{t:.3f}s' for t in result['times']]}")

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    # Calculate overall statistics
    total_time = sum(r['avg_time'] for r in results)
    fastest = results[0]
    slowest = results[-1]
    
    print(f"\nFastest rule: {fastest['rule_folder']} ({fastest['avg_time']:.3f}s average)")
    print(f"Slowest rule: {slowest['rule_folder']} ({slowest['avg_time']:.3f}s average)")
    print(f"Speed difference: {slowest['avg_time'] / fastest['avg_time']:.1f}x")
    print(f"\nTotal average time across all rules: {total_time:.3f}s")
    print()


def get_user_input():
    """
    Get the number of iterations and timeout from user input or command line arguments.

    Returns:
        tuple: (num_iterations, timeout)
    """
    num_iterations = 5
    timeout = DEFAULT_TIMEOUT
    
    # Check command line arguments first
    if len(sys.argv) > 1:
        # Parse arguments
        args = sys.argv[1:]
        i = 0
        while i < len(args):
            if args[i] == '--timeout' and i + 1 < len(args):
                try:
                    timeout = int(args[i + 1])
                    if timeout < 1:
                        print("Timeout must be at least 1 second. Using default of 120.")
                        timeout = DEFAULT_TIMEOUT
                except ValueError:
                    print(f"Invalid timeout '{args[i + 1]}'. Using default of 120.")
                i += 2
            elif args[i] == '--help' or args[i] == '-h':
                print(__doc__)
                sys.exit(0)
            else:
                try:
                    num_iterations = int(args[i])
                    if num_iterations < 1:
                        print("Number of iterations must be at least 1. Using default of 5.")
                        num_iterations = 5
                except ValueError:
                    print(f"Invalid argument '{args[i]}'. Use --help for usage.")
                    sys.exit(1)
                i += 1
        
        return num_iterations, timeout
    
    # Interactive prompt
    print("=" * 70)
    print("SUDOKU PERFORMANCE TEST")
    print("=" * 70)
    print()
    print("This script will test the generation time for all Sudoku rules.")
    print("More iterations give more accurate averages but take longer.")
    print()
    
    while True:
        try:
            user_input = input("Enter number of sudokus to generate per rule [default: 5]: ").strip()
            if user_input == "":
                num_iterations = 5
            else:
                num_iterations = int(user_input)
                if num_iterations < 1:
                    print("Please enter a number >= 1")
                    continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit(0)
    
    while True:
        try:
            user_input = input(f"Enter timeout per generation in seconds [default: {DEFAULT_TIMEOUT}]: ").strip()
            if user_input == "":
                timeout = DEFAULT_TIMEOUT
            else:
                timeout = int(user_input)
                if timeout < 1:
                    print("Please enter a number >= 1")
                    continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit(0)
    
    return num_iterations, timeout


if __name__ == "__main__":
    num_iterations, timeout = get_user_input()
    print()
    run_performance_test(num_iterations=num_iterations, timeout=timeout, verbose=False)

