from flask import Flask, render_template
import random
import os
import ast

app = Flask(__name__)

position_classes = [
    'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6',
    'pos7', 'pos8', 'pos9', 'pos10', 'pos11', 'pos12',
    'pos13', 'pos14', 'pos15', 'pos16', 'pos17', 'pos18',
    'pos19', 'pos20', 'pos21', 'pos22', 'pos23', 'pos24',
]

def load_sudoku():
    """Load sudoku puzzle from text file."""
    path = os.path.join(os.path.dirname(__file__),
                        '..',
                        'custom_sudoku_generator',
                        'sudoku_knights_rule',
                        'sudoku.txt')
    grid = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = ast.literal_eval(line)
            grid.append(row)
    return grid

def load_solution():
    """Load sudoku solution from text file."""
    path = os.path.join(os.path.dirname(__file__),
                        '..',
                        'custom_sudoku_generator',
                        'sudoku_knights_rule',
                        'solution.txt')
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
    shuffled_doors = list(range(1, 25))
    random.shuffle(shuffled_doors)
    # Pass list of tuples (door_number, position_class)
    door_positions = list(zip(shuffled_doors, position_classes))
    return render_template("calendar.html", door_positions=door_positions)

@app.route('/door/<int:door_number>')
def door(door_number):
    # For door 1, load and display the interactive sudoku
    if door_number == 1:
        sudoku_grid = load_sudoku()
        solution_grid = load_solution()
        return render_template("door1.html", door=door_number, sudoku=sudoku_grid, solution=solution_grid)
    # For other doors, render their specific templates
    return render_template(f"door{door_number}.html", door=door_number)

if __name__ == "__main__":
    app.run(debug=True)
