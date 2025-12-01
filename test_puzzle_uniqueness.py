#!/usr/bin/env python
"""Test that all puzzles have exactly one solution."""

import sys
import os
import ast
import copy
import json

# Add the custom_sudoku_generator directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_sudoku_generator'))

from run import SudokuGenerator, load_custom_rule, discover_rules
from base_rule import BaseRule


def load_constraints_from_metadata(rule_folder, custom_rule):
    """
    Load constraints from metadata.json into the custom rule instance.
    This is needed because derived constraints are saved to metadata but 
    not automatically restored when loading the rule.
    """
    metadata_path = os.path.join(rule_folder, 'metadata.json')
    if not os.path.exists(metadata_path):
        return
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    rule_data = metadata.get('rule', {})
    
    # Handle thermometers (list of lists of cells that need to be tuples)
    if 'thermometers' in rule_data:
        custom_rule.thermometers = [
            [tuple(cell) for cell in thermo]
            for thermo in rule_data['thermometers']
        ]
    
    # Handle whisper_lines (list of lists of cells that need to be tuples)
    if 'whisper_lines' in rule_data:
        custom_rule.whisper_lines = [
            [tuple(cell) for cell in line]
            for line in rule_data['whisper_lines']
        ]
    
    # Handle consecutive_lines (list of lists of cells that need to be tuples)
    if 'consecutive_lines' in rule_data:
        custom_rule.consecutive_lines = [
            [tuple(cell) for cell in line]
            for line in rule_data['consecutive_lines']
        ]
    
    # Handle renban_lines (list of lists of cells that need to be tuples)
    if 'renban_lines' in rule_data:
        custom_rule.renban_lines = [
            [tuple(cell) for cell in line]
            for line in rule_data['renban_lines']
        ]
    
    # Handle even_cells and odd_cells (lists of cells that need to be tuples)
    if 'even_cells' in rule_data:
        custom_rule.even_cells = [tuple(cell) for cell in rule_data['even_cells']]
    if 'odd_cells' in rule_data:
        custom_rule.odd_cells = [tuple(cell) for cell in rule_data['odd_cells']]
    
    # Handle x_pairs and v_pairs (list of pairs of cells)
    if 'x_pairs' in rule_data:
        custom_rule.x_pairs = [
            (tuple(pair[0]), tuple(pair[1]))
            for pair in rule_data['x_pairs']
        ]
    if 'v_pairs' in rule_data:
        custom_rule.v_pairs = [
            (tuple(pair[0]), tuple(pair[1]))
            for pair in rule_data['v_pairs']
        ]
    
    # Handle arrows (list of dictionaries with circle and arrow_cells)
    if 'arrows' in rule_data:
        arrows = []
        for arrow in rule_data['arrows']:
            # The validate method expects tuple pairs (circle, arrow_cells)
            arrows.append((
                tuple(arrow['circle']),
                [tuple(cell) for cell in arrow['arrow_cells']]
            ))
        custom_rule.arrows = arrows
    
    # Handle inequalities (list of dictionaries with cell1, cell2, operator)
    if 'inequalities' in rule_data:
        inequalities = []
        for ineq in rule_data['inequalities']:
            inequalities.append((
                tuple(ineq['cell1']),
                tuple(ineq['cell2']),
                ineq['operator']
            ))
        custom_rule.inequalities = inequalities
    
    # Handle cages (list of dictionaries with cells and sum)
    # The killer rule expects cages as list of (sum, cells) tuples
    # and also needs cell_to_cage dict for fast lookups
    if 'cages' in rule_data:
        cages = []
        cell_to_cage = {}
        for cage_idx, cage in enumerate(rule_data['cages']):
            cells = [tuple(cell) for cell in cage['cells']]
            cage_sum = cage['sum']
            cages.append((cage_sum, cells))
            for cell in cells:
                cell_to_cage[cell] = cage_idx
        custom_rule.cages = cages
        custom_rule.cell_to_cage = cell_to_cage
    
    # Handle kropki dots (list of pairs)
    if 'white_dots' in rule_data:
        custom_rule.white_dots = [
            (tuple(dot[0]), tuple(dot[1])) for dot in rule_data['white_dots']
        ]
    if 'black_dots' in rule_data:
        custom_rule.black_dots = [
            (tuple(dot[0]), tuple(dot[1])) for dot in rule_data['black_dots']
        ]
    
    # Handle sandwich clues (dict with string keys like "row_0", "col_2")
    # The sandwich rule expects tuple keys like ('row', 0), ('col', 2)
    if 'sandwich_clues' in rule_data:
        sandwich_clues = {}
        for key, value in rule_data['sandwich_clues'].items():
            parts = key.split('_')
            direction = parts[0]
            index = int(parts[1])
            sandwich_clues[(direction, index)] = value
        custom_rule.sandwich_clues = sandwich_clues
    
    # Handle jigsaw regions (list of lists of cells that need to be tuples)
    if 'jigsaw_regions' in rule_data:
        custom_rule.jigsaw_regions = [
            [tuple(cell) for cell in region]
            for region in rule_data['jigsaw_regions']
        ]
    
    # Special handling for use_standard_boxes
    if 'use_standard_boxes' in rule_data:
        custom_rule.use_standard_boxes = rule_data['use_standard_boxes']


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
        
        # Load constraints from metadata.json
        load_constraints_from_metadata(rule_folder, custom_rule)
        
        # Create a generator with the custom rule
        gen = SudokuGenerator(custom_rule=custom_rule)
        # Reset timeout state to ensure accurate solution counting
        gen.reset_timeout()
        
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
