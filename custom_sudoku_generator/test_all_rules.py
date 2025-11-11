#!/usr/bin/env python
"""
Test all Sudoku rules to identify slow or failing ones.
"""

import time
import signal
import sys
from run import discover_rules, generate_sudoku_for_rule


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError()


def test_rule(rule_folder, timeout_seconds=20):
    """Test a single rule with timeout."""
    rule_name = rule_folder.split('/')[-1]

    # Set up timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)

    start = time.time()
    try:
        generate_sudoku_for_rule(rule_folder)
        elapsed = time.time() - start
        signal.alarm(0)  # Cancel alarm
        return 'success', elapsed
    except TimeoutError:
        signal.alarm(0)
        return 'timeout', timeout_seconds
    except Exception as e:
        signal.alarm(0)
        return 'error', str(e)


def main():
    rules = sorted(discover_rules())
    print(f'Testing {len(rules)} rules (20s timeout each)...\n')
    print('=' * 70)

    results = {
        'fast': [],      # < 2s
        'ok': [],        # 2-5s
        'slow': [],      # 5-20s
        'timeout': [],   # > 20s
        'error': []      # errors
    }

    for rule_folder in rules:
        rule_name = rule_folder.split('/')[-1]
        print(f'{rule_name:35s}', end=' ', flush=True)

        status, info = test_rule(rule_folder)

        if status == 'success':
            elapsed = info
            if elapsed < 2:
                print(f'✓ {elapsed:.2f}s')
                results['fast'].append((rule_name, elapsed))
            elif elapsed < 5:
                print(f'○ {elapsed:.2f}s')
                results['ok'].append((rule_name, elapsed))
            else:
                print(f'⚠ {elapsed:.2f}s')
                results['slow'].append((rule_name, elapsed))
        elif status == 'timeout':
            print('✗ TIMEOUT (>20s)')
            results['timeout'].append(rule_name)
        else:  # error
            print(f'✗ ERROR: {info}')
            results['error'].append((rule_name, info))

    # Summary
    print('\n' + '=' * 70)
    print('SUMMARY')
    print('=' * 70)

    print(f"\n✓ Fast (<2s): {len(results['fast'])} rules")
    for name, t in results['fast']:
        print(f"  {name:30s} {t:.2f}s")

    print(f"\n○ OK (2-5s): {len(results['ok'])} rules")
    for name, t in results['ok']:
        print(f"  {name:30s} {t:.2f}s")

    if results['slow']:
        print(f"\n⚠ Slow (5-20s): {len(results['slow'])} rules - NEED OPTIMIZATION")
        for name, t in results['slow']:
            print(f"  {name:30s} {t:.2f}s")

    if results['timeout']:
        print(f"\n✗ Timeout (>20s): {len(results['timeout'])} rules - NEED FIX")
        for name in results['timeout']:
            print(f"  {name}")

    if results['error']:
        print(f"\n✗ Errors: {len(results['error'])} rules - NEED FIX")
        for name, err in results['error']:
            print(f"  {name}: {err}")

    print('\n' + '=' * 70)
    total_good = len(results['fast']) + len(results['ok'])
    total = len(rules)
    print(f"Overall: {total_good}/{total} rules working well ({100*total_good//total}%)")

    return len(results['timeout']) + len(results['error'])


if __name__ == '__main__':
    sys.exit(main())

