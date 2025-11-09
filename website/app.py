from flask import Flask, render_template
import random

app = Flask(__name__)

position_classes = [
    'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6',
    'pos7', 'pos8', 'pos9', 'pos10', 'pos11', 'pos12',
    'pos13', 'pos14', 'pos15', 'pos16', 'pos17', 'pos18',
    'pos19', 'pos20', 'pos21', 'pos22', 'pos23', 'pos24',
]

@app.route('/')
def calendar():
    shuffled_doors = list(range(1, 25))
    random.shuffle(shuffled_doors)
    # Pass list of tuples (door_number, position_class)
    door_positions = list(zip(shuffled_doors, position_classes))
    return render_template("calendar.html", door_positions=door_positions)

@app.route('/door/<int:door_number>')
def door(door_number):
    # Render a template for that door (custom content per door)
    return render_template(f"door{door_number}.html", door=door_number)

if __name__ == "__main__":
    app.run(debug=True)
