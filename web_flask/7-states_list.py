#!/usr/bin/python3
"""
Flask web application to display a list of states.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(self):
    """Closes the storage on teardown"""
    from models import storage
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    from models.state import State
    from models import storage
    """Displays an HTML page with a list of states sorted by name"""
    return render_template('7-states_list.html',
                           states=storage.all(State))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
