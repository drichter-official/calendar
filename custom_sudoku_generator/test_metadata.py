#!/usr/bin/env python3
"""
Test script to verify all rules have complete metadata with special cells.
"""
import os
import json
import sys

# Expected metadata fields for each rule type
EXPECTED_FIELDS = {
    'argyle': ['argyle_cells'],
    'arrow': ['arrows'],
    'asterisk': ['asterisk_cells'],
    'center_dot': ['center_dot_cells'],
    'chain': ['corner_cells'],
    'consecutive': ['consecutive_pairs'],
    'diagonal': ['diagonal_cells'],
    'even_odd': ['even_cells', 'odd_cells'],
    'futoshiki': ['inequalities'],
    'jigsaw': ['jigsaw_regions'],
    'killer': ['cages'],
    'kropki': ['white_dots', 'black_dots'],
    'magic_square': ['magic_box_location'],
    'renban': ['renban_lines'],
    'sandwich': ['sandwich_clues'],
    'star': ['star_cells'],
    'thermo': ['thermometers'],
    'whisper': ['whisper_lines'],
    'windoku': ['windoku_regions'],
    'xv': ['x_pairs', 'v_pairs'],
    # Rules without special cells (global constraints)
    'kings': [],
    'knights': [],
    'nonconsecutive': [],
    'skyscraper': [],
}

def get_rule_type(rule_name):
    """Extract rule type from folder name."""
    if rule_name.startswith('sudoku_'):
        rule_name = rule_name[7:]
    if rule_name.endswith('_rule'):
        rule_name = rule_name[:-5]
    return rule_name

def check_metadata(rule_dir):
    """Check if a rule's metadata has all expected fields."""
    rule_type = get_rule_type(os.path.basename(rule_dir.rstrip('/')))
    metadata_path = os.path.join(rule_dir, 'metadata.json')
    
    if not os.path.exists(metadata_path):
        return False, f"No metadata.json found"
    
    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
    except Exception as e:
        return False, f"Failed to parse JSON: {e}"
    
    if 'rule' not in metadata:
        return False, "No 'rule' key in metadata"
    
    rule_data = metadata['rule']
    
    # Check basic fields
    if 'name' not in rule_data or 'description' not in rule_data:
        return False, "Missing 'name' or 'description'"
    
    # Check special cell fields
    expected = EXPECTED_FIELDS.get(rule_type, [])
    missing = []
    for field in expected:
        if field not in rule_data:
            missing.append(field)
    
    if missing:
        return False, f"Missing special cell fields: {', '.join(missing)}"
    
    return True, "OK"

def main():
    """Test all rules."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all rule folders
    rule_folders = []
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        if os.path.isdir(item_path) and item.startswith('sudoku_') and item.endswith('_rule'):
            rule_folders.append(item_path)
    
    rule_folders.sort()
    
    print(f"Testing {len(rule_folders)} rule folders...")
    print("=" * 80)
    
    passed = []
    failed = []
    
    for rule_dir in rule_folders:
        rule_name = os.path.basename(rule_dir)
        success, message = check_metadata(rule_dir)
        
        if success:
            print(f"✓ {rule_name:30s} - {message}")
            passed.append(rule_name)
        else:
            print(f"✗ {rule_name:30s} - {message}")
            failed.append((rule_name, message))
    
    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Passed: {len(passed)}/{len(rule_folders)}")
    print(f"  Failed: {len(failed)}/{len(rule_folders)}")
    
    if failed:
        print(f"\nFailed rules:")
        for rule_name, message in failed:
            print(f"  - {rule_name}: {message}")
        sys.exit(1)
    else:
        print("\n✓ All rules have complete metadata!")
        sys.exit(0)

if __name__ == '__main__':
    main()
