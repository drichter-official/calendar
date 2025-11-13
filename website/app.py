from flask import Flask, render_template, jsonify, request
import random
import os
import ast
import sys

app = Flask(__name__)

# Error handler for all exceptions on /generate routes
@app.errorhandler(Exception)
def handle_error(e):
    # Only return JSON for API routes
    if '/generate/' in request.path:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500
    # For other routes, let Flask handle it normally
    raise e

# Add the custom_sudoku_generator to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'custom_sudoku_generator'))

# Mapping of door numbers to rule folders
DOOR_TO_RULE = {
    1: 'sudoku_knights_rule',
    2: 'sudoku_diagonal_rule',
    3: 'sudoku_windoku_rule',
    4: 'sudoku_asterisk_rule',
    5: 'sudoku_kings_rule',
    6: 'sudoku_argyle_rule',
    7: 'sudoku_center_dot_rule',
    8: 'sudoku_star_rule',
    9: 'sudoku_magic_square_rule',
    10: 'sudoku_nonconsecutive_rule',
    11: 'sudoku_consecutive_rule',
    12: 'sudoku_even_odd_rule',
    13: 'sudoku_kropki_rule',
    14: 'sudoku_xv_rule',
    15: 'sudoku_sandwich_rule',
    16: 'sudoku_skyscraper_rule',
    17: 'sudoku_futoshiki_rule',
    18: 'sudoku_killer_rule',
    19: 'sudoku_arrow_rule',
    20: 'sudoku_chain_rule',
    21: 'sudoku_thermo_rule',
    22: 'sudoku_whisper_rule',
    23: 'sudoku_renban_rule',
    24: 'sudoku_jigsaw_rule',
}

def get_rule_folder(door_number):
    """Get the rule folder path for a given door number."""
    rule_name = DOOR_TO_RULE.get(door_number, 'sudoku_knights_rule')
    return os.path.join(os.path.dirname(__file__), '..', 'custom_sudoku_generator', rule_name)

def load_metadata(door_number):
    """Load metadata for a given door number."""
    rule_folder = get_rule_folder(door_number)
    metadata_path = os.path.join(rule_folder, 'metadata.json')
    try:
        import json
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load metadata for door {door_number}: {e}")
        return {
            'rule': {
                'name': 'Interactive Sudoku',
                'description': 'Fill in the empty cells with numbers 1-9. Each row, column, and 3x3 box must contain all digits from 1 to 9.'
            }
        }

position_classes = [
    'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6',
    'pos7', 'pos8', 'pos9', 'pos10', 'pos11', 'pos12',
    'pos13', 'pos14', 'pos15', 'pos16', 'pos17', 'pos18',
    'pos19', 'pos20', 'pos21', 'pos22', 'pos23', 'pos24',
]

def load_sudoku(door_number=1):
    """Load sudoku puzzle from text file."""
    rule_folder = get_rule_folder(door_number)
    path = os.path.join(rule_folder, 'sudoku.txt')
    grid = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = ast.literal_eval(line)
            grid.append(row)
    return grid

def load_solution(door_number=1):
    """Load sudoku solution from text file."""
    rule_folder = get_rule_folder(door_number)
    path = os.path.join(rule_folder, 'solution.txt')
    grid = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = ast.literal_eval(line)
            grid.append(row)
    return grid

@app.route('/')
def calendar():
    doors = list(range(1, 25))
    # Pass list of tuples (door_number, position_class)
    door_positions = list(zip(doors, position_classes))
    return render_template("calendar.html", door_positions=door_positions)

@app.route('/door/<int:door_number>')
def door(door_number):
    # Validate door number
    if door_number < 1 or door_number > 24:
        return "Invalid door number", 404
    
    # Load metadata, sudoku grid, and solution for the door
    metadata = load_metadata(door_number)
    sudoku_grid = load_sudoku(door_number)
    solution_grid = load_solution(door_number)
    
    # Use a generic template for all doors
    return render_template("door.html", 
                         door=door_number, 
                         metadata=metadata,
                         sudoku=sudoku_grid, 
                         solution=solution_grid)

@app.route('/generate/<int:door_number>')
def generate_puzzle(door_number):
    """Generate a new sudoku puzzle for the specified door."""
    try:
        # Check if we have write permissions
        rule_folder = get_rule_folder(door_number)

        # Ensure the rule folder exists
        if not os.path.exists(rule_folder):
            return jsonify({
                'success': False,
                'message': f'Rule folder not found: {rule_folder}'
            }), 404

        # Check write permissions by trying to create a test file
        test_file = os.path.join(rule_folder, '.write_test')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except (IOError, OSError) as e:
            return jsonify({
                'success': False,
                'message': f'No write permission in rule folder. Please check file permissions on the server.'
            }), 403

        # Import the generation function
        try:
            from run import generate_sudoku_for_rule
        except ImportError as e:
            return jsonify({
                'success': False,
                'message': f'Could not import generation module: {str(e)}'
            }), 500

        # Generate new puzzle
        print(f"Generating new puzzle for door {door_number}...")
        print(f"Rule folder: {rule_folder}")
        puzzle_grid, solution_grid = generate_sudoku_for_rule(rule_folder)

        return jsonify({
            'success': True,
            'message': 'New puzzle generated successfully!'
        })
    except Exception as e:
        print(f"Error generating puzzle: {e}")
        import traceback
        traceback.print_exc()

        # Return a proper JSON error response
        error_message = str(e)
        if len(error_message) > 200:
            error_message = error_message[:200] + '...'

        return jsonify({
            'success': False,
            'message': f'Error: {error_message}'
        }), 500

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000, debug = True)
