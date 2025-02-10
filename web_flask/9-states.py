#!/usr/bin/python3
"""Starts a Flask web application to display states and cities"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Displays a HTML page listing all states sorted by name"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays a HTML page of a specific state and its cities"""
    states = storage.all(State)
    state = states.get(f"State.{id}")
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)\
                 if hasattr(state, 'cities') else []
        return render_template('9-states.html', state=state, cities=cities)
    return render_template('9-states.html', not_found=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
