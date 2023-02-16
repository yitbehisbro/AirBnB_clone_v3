#!/usr/bin/python3
""" Index file module """
from api.v1.views.__init__ import app_views
from flask import jsonify
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Displays the status """
    stat = {"status": "OK"}
    return jsonify(stat)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Displays the status """
    dic = {"amenities": storage.count(Amenity),
           "cities": storage.count(City),
           "places": storage.count(Place),
           "reviews": storage.count(Review),
           "states": storage.count(State),
           "users": storage.count(User)}
    return jsonify(dic)
