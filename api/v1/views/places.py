#!/usr/bin/python3
""" Aminity view module """
from models.place import Place
from models.city import City
from models import storage
from api.v1.views.__init__ import app_views
from flask import jsonify
from flask import abort
from flask import request
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def p_display(city_id):
    """ Retrieves the list of a class objects """
    get_city = storage.get(City.__name__, city_id)
    if not get_city:
        abort(404)
    return jsonify([place.to_dict() for place in get_city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def p_display_by_id(place_id):
    """ Retrieves the list of a class objects """
    get_place = storage.get(Place.__name__, place_id)
    if not get_place:
        abort(404)
    return jsonify(get_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def p_delete_by_id(place_id):
    """ Deletes a 'class' object """
    get_place = storage.get(Place.__name__, place_id)
    if not get_place:
        abort(404)
    get_place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def p_post_request(city_id):
    """ Posts a 'class' object """
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')
    """user_id = kwargs['user_id']
    if not storage.get(User.__name__, user_id):
        abort(404)"""
    get_places = Place(**kwargs)
    setattr(get_places, 'city_id', city_id)
    storage.new(get_places)
    storage.save()
    return jsonify(get_places.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def p_put_request(place_id):
    """ Puts a 'class' object """
    get_places = storage.get(Place.__name__, place_id)
    if not get_places:
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    for k, v in kwargs.items():
        if k != 'id' and k != 'user_id' and k != 'created_at'\
                and k != 'updated_at':
            setattr(get_places, k, v)
    storage.save()
    return jsonify(get_places.to_dict()), 200
