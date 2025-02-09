#!/usr/bin/python3
"""Starts a Flask web application to display cities by states"""
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    from models import storage
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    from models.state import State
    from models import storage
    """Displays a HTML page listing states and their cities"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
