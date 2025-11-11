#!/usr/bin/env python
"""Test script to verify all doors work correctly with proper metadata."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from website.app import app

def test_all_doors():
    """Test all 24 doors to ensure they load correctly."""
    with app.test_client() as client:
        print("Testing all 24 doors...\n")
        all_pass = True
        
        for door in range(1, 25):
            response = client.get(f'/door/{door}')
            
            if response.status_code == 200:
                # Check that metadata is present
                data = response.data.decode('utf-8')
                if 'Day ' + str(door) in data:
                    print(f'✓ Door {door:2d}: SUCCESS')
                else:
                    print(f'✗ Door {door:2d}: FAIL - Missing door number')
                    all_pass = False
            else:
                print(f'✗ Door {door:2d}: FAIL - Status {response.status_code}')
                all_pass = False
        
        return all_pass

def test_special_highlighting_doors():
    """Test doors with special cell highlighting."""
    with app.test_client() as client:
        print("\n\nTesting doors with special highlighting...\n")
        
        special_doors = {
            2: 'diagonal-cell',  # Diagonal rule
            3: 'special-cell',   # Windoku
            4: 'special-cell',   # Asterisk
            12: 'special-cell',  # Even-Odd
        }
        
        all_pass = True
        for door, css_class in special_doors.items():
            response = client.get(f'/door/{door}')
            data = response.data.decode('utf-8')
            
            # Check for the highlighting class or the metadata that triggers it
            if css_class in data or 'applySpecialCellHighlighting' in data:
                print(f'✓ Door {door:2d}: Has highlighting support')
            else:
                print(f'✗ Door {door:2d}: Missing highlighting support')
                all_pass = False
        
        return all_pass

def test_metadata_content():
    """Test that metadata is correctly loaded for all doors."""
    from website.app import load_metadata
    
    print("\n\nTesting metadata loading...\n")
    
    all_pass = True
    for door in range(1, 25):
        metadata = load_metadata(door)
        if 'rule' in metadata and 'name' in metadata['rule'] and 'description' in metadata['rule']:
            rule_name = metadata['rule']['name']
            print(f'✓ Door {door:2d}: {rule_name}')
        else:
            print(f'✗ Door {door:2d}: Missing metadata')
            all_pass = False
    
    return all_pass

def test_invalid_door():
    """Test that invalid door numbers return 404."""
    with app.test_client() as client:
        print("\n\nTesting invalid door numbers...\n")
        
        # Test positive invalid doors
        for invalid_door in [0, 25, 100]:
            response = client.get(f'/door/{invalid_door}')
            if response.status_code == 404:
                print(f'✓ Door {invalid_door}: Correctly returns 404')
            else:
                print(f'✗ Door {invalid_door}: Should return 404, got {response.status_code}')
                return False
        
        return True

if __name__ == '__main__':
    results = []
    
    results.append(("All Doors Load", test_all_doors()))
    results.append(("Metadata Loading", test_metadata_content()))
    results.append(("Special Highlighting", test_special_highlighting_doors()))
    results.append(("Invalid Doors", test_invalid_door()))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
