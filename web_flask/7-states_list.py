#!/usr/bin/python3
"""Starts a Flask web application to display States list"""
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the current SQLAlchemy Session after each request."""
    from models import storage
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    from models import storage
    from models.state import State
    """Display a HTML page with the list of all State objects."""
    states = storage.all(State).values()
    return render_template('7-states_list.html',
                           states=sorted(states, key=lambda state: state.name))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
