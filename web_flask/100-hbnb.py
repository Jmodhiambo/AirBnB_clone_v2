#!/usr/bin/python3
"""Starts a Flask web application for the HBNB clone"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays an HTML page with States, Amenities, and Places"""
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda a: a.name)
    places = sorted(storage.all(Place).values(), key=lambda p: p.name)
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
