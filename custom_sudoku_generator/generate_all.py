#!/usr/bin/env python3
"""
Script to generate all Sudoku variants with timeout protection.
"""
import subprocess
import sys
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get all rule folders
rule_folders = []
for item in os.listdir(script_dir):
    item_path = os.path.join(script_dir, item)
    if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "rule.py")):
        rule_folders.append(item_path)

rule_folders.sort()

print(f"Found {len(rule_folders)} rule folders")
print("="*60)

successful = []
failed = []
skipped = []

for i, folder in enumerate(rule_folders, 1):
    rule_name = os.path.basename(folder)
    print(f"\n[{i}/{len(rule_folders)}] Generating {rule_name}...")
    
    # Check if already generated
    metadata_file = os.path.join(folder, "metadata.json")
    if os.path.exists(metadata_file):
        print(f"  ✓ Already generated, skipping")
        skipped.append(rule_name)
        continue
    
    try:
        # Run with 120 second timeout
        result = subprocess.run(
            [sys.executable, "run.py", folder, "5"],
            cwd=script_dir,
            timeout=120,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and os.path.exists(metadata_file):
            print(f"  ✓ Success")
            successful.append(rule_name)
        else:
            print(f"  ✗ Failed: {result.stderr[:200] if result.stderr else 'Unknown error'}")
            failed.append(rule_name)
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout (rule too restrictive)")
        failed.append(rule_name)
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:200]}")
        failed.append(rule_name)

print("\n" + "="*60)
print(f"\nSummary:")
print(f"  Successful: {len(successful)}")
print(f"  Skipped (already generated): {len(skipped)}")
print(f"  Failed: {len(failed)}")

if failed:
    print(f"\nFailed rules:")
    for rule in failed:
        print(f"  - {rule}")

total_generated = len(successful) + len(skipped)
print(f"\nTotal generated: {total_generated}/{len(rule_folders)}")
