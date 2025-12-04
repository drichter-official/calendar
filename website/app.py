from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_babel import Babel
from datetime import datetime
import pytz
import os
import ast
import sys

app = Flask(__name__)

# =============================================================================
# DOOR TIME RESTRICTION CONFIGURATION
# =============================================================================
# Set to True to enable time-based door restrictions (doors unlock at 6 AM CET on their day)
# Set to False to disable the feature (all doors accessible at any time)
ENABLE_DOOR_TIME_RESTRICTION = True
# =============================================================================
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['BABEL_DEFAULT_LOCALE'] = 'de'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'de']

def get_locale():
    # Try to get locale from session first, then from request
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or 'de'

babel = Babel(app, locale_selector=get_locale)

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
    1: 'sudoku_standard_rule',
    2: 'sudoku_diagonal_rule',
    3: 'sudoku_windoku_rule',
    4: 'sudoku_asterisk_rule',
    5: 'sudoku_consecutive_rule',
    6: 'sudoku_argyle_rule',
    7: 'sudoku_center_dot_rule',
    8: 'sudoku_star_rule',
    9: 'sudoku_magic_square_rule',
    10: 'sudoku_nonconsecutive_rule',
    11: 'sudoku_kings_rule',
    12: 'sudoku_even_odd_rule',
    13: 'sudoku_kropki_rule',
    14: 'sudoku_xv_rule',
    15: 'sudoku_sandwich_rule',
    16: 'sudoku_knights_rule',
    17: 'sudoku_futoshiki_rule',
    18: 'sudoku_killer_rule',
    19: 'sudoku_arrow_rule',
    20: 'sudoku_offset_rule',
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


german_translations = {
        'sudoku_standard_rule': {'name': 'Standard Sudoku',
                                 'description': 'Fülle das Gitter so aus, dass jede Zeile, Spalte und 3x3-Box die Ziffern 1-9 enthält'},
        'sudoku_knights_rule': {'name': 'Anti-Springer Sudoku',
                                'description': 'Gleiche Zahlen dürfen nicht durch einen Springer-Sprung (Schach) verbunden sein'},
        'sudoku_diagonal_rule': {'name': 'Diagonal Sudoku',
                                 'description': 'Beide Hauptdiagonalen müssen alle Ziffern von 1 bis 9 enthalten'},
        'sudoku_windoku_rule': {'name': 'Windoku',
                                'description': 'Vier zusätzliche 3x3-Regionen müssen ebenfalls alle Ziffern von 1 bis 9 enthalten'},
        'sudoku_asterisk_rule': {'name': 'Sternchen Sudoku',
                                 'description': 'Die 9 Sternchen-Zellen müssen alle Ziffern von 1 bis 9 enthalten'},
        'sudoku_kings_rule': {'name': 'Anti Königs Sudoku',
                              'description': 'Gleiche Zahlen dürfen nicht durch einen König-Zug (Schach) verbunden sein'},
        'sudoku_argyle_rule': {'name': 'Argyle Sudoku',
                               'description': 'Diagonalen innerhalb jeder 3x3-Box müssen eindeutige Zahlen haben'},
        'sudoku_center_dot_rule': {'name': 'Mittelpunkt Sudoku',
                                   'description': 'Die mittlere Zelle jeder 3x3-Box muss eine eindeutige Zahl enthalten'},
        'sudoku_star_rule': {'name': 'Stern Sudoku',
                             'description': 'Der Stern muss alle Ziffern von 1 bis 9 enthalten'},
        'sudoku_magic_square_rule': {'name': 'Magisches Quadrat Sudoku',
                                     'description': 'Das 3x3-Quadrat in der Mitte muss ein magisches Quadrat sein (Summe 15)'},
        'sudoku_nonconsecutive_rule': {'name': 'Nicht Aufeinanderfolgendes Sudoku',
                                       'description': 'Aufeinanderfolgende Zahlen dürfen sich nicht orthogonal berühren'},
        'sudoku_consecutive_rule': {'name': 'Aufeinanderfolgendes Sudoku',
                                    'description': 'Markierte Linien enthalten aufeinanderfolgende Zahlen'},
        'sudoku_even_odd_rule': {'name': 'Gerade Ungerade Sudoku',
                                 'description': 'Markierte Zellen müssen gerade oder ungerade Zahlen enthalten'},
        'sudoku_kropki_rule': {'name': 'Kropki Sudoku',
                               'description': 'Weiße Punkte: aufeinanderfolgende Zahlen, Schwarze Punkte: Verhältnis 1:2'},
        'sudoku_xv_rule': {'name': 'XV Sudoku',
                           'description': 'Bestimmte benachbarte Zellen müssen sich zu 10 (X) oder 5 (V) summieren'},
        'sudoku_sandwich_rule': {'name': 'Sandwich-Sudoku',
                                 'description': 'Zahlen zwischen 1 und 9 in einer Reihe/Spalte summieren sich zu gegebenen Hinweisen'},
        'sudoku_futoshiki_rule': {'name': 'Futoshiki Sudoku',
                                  'description': 'Ungleichheitszeichen zeigen Beziehungen zwischen benachbarten Zellen'},
        'sudoku_killer_rule': {'name': 'Killer Sudoku',
                               'description': 'Käfige müssen sich zu angegebenen Summen addieren, ohne wiederholte Ziffern'},
        'sudoku_arrow_rule': {'name': 'Pfeil Sudoku',
                              'description': 'Die Summe entlang des Pfeils muss gleich der Zahl im Kreis sein'},
        'sudoku_offset_rule': {'name': 'Versatz Sudoku',
                              'description': 'Zellen an gleicher Position in jeder 3x3-Box müssen die Ziffern 1-9 enthalten'},
        'sudoku_thermo_rule': {'name': 'Thermometer Sudoku',
                               'description': 'Zahlen müssen entlang von Thermometern von der Zwiebel aufsteigen'},
        'sudoku_whisper_rule': {'name': 'Flüster Sudoku',
                                'description': 'Benachbarte Zellen auf Linien müssen sich um mindestens 5 unterscheiden'},
        'sudoku_renban_rule': {'name': 'Renban Sudoku',
                               'description': 'Linien enthalten aufeinanderfolgende Zahlen in beliebiger Reihenfolge'},
        'sudoku_jigsaw_rule': {'name': 'Puzzle Sudoku',
                               'description': 'Unregelmäßige Regionen ersetzen 3x3-Boxen, müssen alle Ziffern 1-9 enthalten'},
}

# German riddles for each door (1-24) - displayed after solving medium/hard puzzles
# Each riddle has a 'riddle' (question) and 'answer' (solution - stored but not displayed on website)
german_riddles = {
    1: {'riddle': 'Ich habe Städte, aber keine Häuser, Wälder, aber keine Bäume, und Wasser, aber keine Fische.', 'answer': 'Karte'},
    2: {'riddle': 'Ich bin immer hungrig und verschlinge alles, was mir gegeben wird, aber wenn ich Wasser trinke, sterbe ich.','answer': 'Feuer'},
    3: {'riddle': 'Ich reise um die Welt, bleibe aber in einer Ecke.', 'answer': 'Briefmarke'},
    4: {'riddle': 'Ich bin immer vor dir, doch du kannst mich nie erreichen.', 'answer': 'Horizont'},
    5: {'riddle': 'Ich bin schwer zu heben, aber leicht zu werfen.', 'answer': 'Blick'},
    6: {'riddle': 'Ich gehe bergauf und bergab, bleibe aber immer am selben Ort.', 'answer': 'Weg'},
    7: {'riddle': 'Ich bin da, bevor du geboren wirst, und bleibe, wenn du längst fort bist.', 'answer': 'Geschichte'},
    8: {'riddle': 'Wenn du mich auf die Seite legst bin ich alles für immer, in zwei Hälften schneidest, bin ich nichts.','answer': '8'},
    9: {'riddle': 'Ich bin zuhause und doch unterwegs auf Papier.', 'answer': 'Brief'},

    10: {'riddle': 'Kämpfst du mit mir, bin ich schwerer zu treffen je mehr du mich hasst.', 'answer': 'Entscheidung'},
    11: {'riddle': 'Je mehr du nimmst, desto mehr lässt du zurück.', 'answer': 'Schritte'},
    12: {'riddle': 'Ich fliege, aber habe keine Flügel.', 'answer': 'Zeit'},
    13: {'riddle': 'Ich kann gebrochen werden, ohne dass ich angefasst werde.', 'answer': 'Versprechen'},
    14: {'riddle': 'Ich habe viele Augen, sehe aber nichts.', 'answer': 'Würfel'},

    15: {'riddle': 'Ich bin voller Löcher, aber halte Wasser.', 'answer': 'Schwamm'},
    16: {'riddle': 'Ich wachse, aber lebe nicht.', 'answer': 'Kristall'},
    17: {'riddle': 'Ich komme, wenn du schläfst, und gehe, wenn du wachst.', 'answer': 'Traum'},
    18: {'riddle': 'Ich laufe, aber habe keine Beine.', 'answer': 'Uhr'},

    19: {'riddle': 'Je länger ich stehe, desto kleiner werde ich.', 'answer': 'Kerze'},
    20: {'riddle': 'Ich bin leicht wie eine Feder, schwer zu halten.', 'answer': 'Atem'},
    21: {'riddle': 'Ich werde leichter, je mehr man mich füllt.', 'answer': 'Ballon'},
    22: {'riddle': 'Ich habe Finger, aber bin kein Mensch.', 'answer': 'Handschuh'},
    23: {'riddle': 'Ich bin unsichtbar, aber du kannst mich fühlen, und manchmal bringe ich dich aus dem Gleichgewicht.', 'answer': 'Wind'},
    24: {'riddle': 'Ich gehöre dir, aber andere benutzen mich häufiger als du.', 'answer': 'Name'},
}

def get_translated_rule_info(door_number):
    """Get translated rule name and description based on current locale."""
    locale = get_locale()

    # Get the rule folder name for this door
    rule_folder_name = DOOR_TO_RULE.get(door_number, 'sudoku_knights_rule')

    # Load metadata to get English names
    metadata = load_metadata(door_number)
    english_name = metadata['rule']['name']
    english_description = metadata['rule']['description']

    if locale == 'de' and rule_folder_name in german_translations:
        return german_translations[rule_folder_name]['name'], german_translations[rule_folder_name]['description']
    else:
        return english_name, english_description

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

@app.route('/set_language/<language>')
def set_language(language):
    if language in app.config['BABEL_SUPPORTED_LOCALES']:
        session['language'] = language
    # Redirect back to the referrer or home page
    return jsonify({'success': True, 'language': language})

def get_opened_doors():
    """Get the set of opened door numbers from the session."""
    if 'opened_doors' not in session:
        session['opened_doors'] = []
    return set(session['opened_doors'])

def mark_door_opened(door_number):
    """Mark a door as opened in the session."""
    if 'opened_doors' not in session:
        session['opened_doors'] = []
    if door_number not in session['opened_doors']:
        session['opened_doors'].append(door_number)
        session.modified = True
    return True

def is_door_unlocked(door_number):
    """
    Check if a door is unlocked based on the current time in CET.
    A door unlocks at 6 AM CET on its corresponding day in December.
    For example, door 1 unlocks at 6 AM CET on December 1st.
    
    Returns True if:
    - ENABLE_DOOR_TIME_RESTRICTION is False (feature disabled)
    - Current CET time is on or after 6 AM on the door's day
    """
    if not ENABLE_DOOR_TIME_RESTRICTION:
        return True
    
    # Validate door number
    if door_number < 1 or door_number > 24:
        return False
    
    # Get current time in CET (Central European Time)
    cet = pytz.timezone('Europe/Berlin')
    now_cet = datetime.now(cet)
    
    # Determine the year for this advent calendar
    # If we're in December, use current year
    # If we're in January (before December's advent calendar ends), use previous year
    # Otherwise, use current year (for testing or future access)
    year = now_cet.year
    if now_cet.month == 1 and now_cet.day <= 7:
        # Early January - still in the advent calendar period, use previous year
        year = now_cet.year - 1
    
    # Create the unlock datetime: December {door_number} at 6:00 AM CET
    try:
        unlock_time = cet.localize(datetime(year, 12, door_number, 6, 0, 0))
    except ValueError:
        # Invalid date (shouldn't happen with doors 1-24)
        return False
    
    # Door is unlocked if current time is at or after the unlock time
    return now_cet >= unlock_time

def get_unlocked_doors():
    """Get a set of door numbers that are currently unlocked based on time."""
    return {door for door in range(1, 25) if is_door_unlocked(door)}

@app.route('/api/opened_doors')
def api_get_opened_doors():
    """API endpoint to get the list of opened doors."""
    opened = list(get_opened_doors())
    return jsonify({'opened_doors': sorted(opened)})

@app.route('/api/door/<int:door_number>/opened', methods=['GET'])
def api_check_door_opened(door_number):
    """API endpoint to check if a specific door is opened."""
    if door_number < 1 or door_number > 24:
        return jsonify({'error': 'Invalid door number'}), 400
    opened = door_number in get_opened_doors()
    return jsonify({'door': door_number, 'opened': opened})

@app.route('/api/close_all_doors', methods=['POST'])
def api_close_all_doors():
    """API endpoint to close all doors (clear the session)."""
    session['opened_doors'] = []
    session.modified = True
    return jsonify({'success': True, 'message': 'All doors closed'})

@app.route('/api/door/<int:door_number>/unlocked', methods=['GET'])
def api_check_door_unlocked(door_number):
    """API endpoint to check if a specific door is unlocked (based on time restriction)."""
    if door_number < 1 or door_number > 24:
        return jsonify({'error': 'Invalid door number'}), 400
    unlocked = is_door_unlocked(door_number)
    return jsonify({'door': door_number, 'unlocked': unlocked, 'restriction_enabled': ENABLE_DOOR_TIME_RESTRICTION})

@app.route('/api/unlocked_doors')
def api_get_unlocked_doors():
    """API endpoint to get the list of unlocked doors (based on time restriction)."""
    unlocked = list(get_unlocked_doors())
    return jsonify({'unlocked_doors': sorted(unlocked), 'restriction_enabled': ENABLE_DOOR_TIME_RESTRICTION})

@app.route('/')
def calendar():
    doors = list(range(1, 25))

    # Fixed mapping: each door always appears at the same position
    # Door number matches position class number (door 1 at pos1, door 2 at pos2, etc.)
    door_positions = list(zip(doors, position_classes))
    opened_doors = get_opened_doors()
    unlocked_doors = get_unlocked_doors()
    return render_template("calendar.html", door_positions=door_positions, opened_doors=opened_doors, unlocked_doors=unlocked_doors, get_locale=get_locale, restriction_enabled=ENABLE_DOOR_TIME_RESTRICTION)

@app.route('/door/<int:door_number>')
def door(door_number):
    # Validate door number
    if door_number < 1 or door_number > 24:
        return "Invalid door number", 404
    
    # Check if door is unlocked (based on time restriction)
    if not is_door_unlocked(door_number):
        # Door is locked, redirect to calendar with an error message
        return redirect(url_for('calendar') + '?locked=' + str(door_number))
    
    # Mark this door as opened
    mark_door_opened(door_number)
    
    # Load metadata, sudoku grid, and solution for the door
    metadata = load_metadata(door_number)
    sudoku_grid = load_sudoku(door_number)
    solution_grid = load_solution(door_number)
    
    # Get translated rule name and description
    rule_name, rule_description = get_translated_rule_info(door_number)
    
    # Get German riddle for this door (only the riddle text, answer not passed to template)
    riddle = german_riddles.get(door_number, {}).get('riddle', '')
    
    # Use a generic template for all doors
    return render_template("door.html", 
                         door=door_number, 
                         metadata=metadata,
                         rule_name=rule_name,
                         rule_description=rule_description,
                         sudoku=sudoku_grid, 
                         solution=solution_grid,
                         riddle=riddle,
                         get_locale=get_locale)

@app.route('/generate/<int:door_number>')
def generate_puzzle(door_number):
    """Generate a new sudoku puzzle for the specified door."""
    try:
        # Get difficulty from query parameter (default to 'hard')
        difficulty = request.args.get('difficulty', 'hard')
        if difficulty not in ('easy', 'medium', 'hard'):
            difficulty = 'hard'
        
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
        print(f"Difficulty: {difficulty}")
        puzzle_grid, solution_grid = generate_sudoku_for_rule(rule_folder, difficulty=difficulty)

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
    app.run( debug = True , host = '0.0.0.0', port = 5001)
