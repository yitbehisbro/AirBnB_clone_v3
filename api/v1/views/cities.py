#!/usr/bin/python3
""" State view module """
from models.city import City
from models.state import State
from models import storage
from api.v1.views.__init__ import app_views
from flask import jsonify
from flask import abort
from flask import request


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_cities(city_id):
    """ Retrieves the list of all 'class' objects"""
    city = storage.get(City.__name__, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def display_by_id1(state_id):
    """ Retrieves the list of a class objects """
    get_state = storage.get(State.__name__, state_id)
    if not get_state:
        abort(404)
    return jsonify([state.to_dict() for state in get_state.cities])


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_by_id1(city_id):
    """ Deletes a 'class' object """
    get_city = storage.get(City.__name__, city_id)
    if not get_city:
        abort(404)

    get_city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_request1(state_id):
    """ Posts a 'class' object """
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    state = kwargs['state_id']
    if state not in storage.get(State.__init__, state_id):
        abort(404)
    get_city = City(**kwargs)
    setattr(get_city, 'state_id', state_id)
    storage.new(get_city)
    storage.save()
    return jsonify(get_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_request1(city_id):
    """ Puts a 'class' object """
    get_city = storage.get(City.__name__, city_id)
    if not get_city:
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    for k, v in kwargs.items():
        if k != 'id' and k != 'state_id'\
                and k != 'created_at' and k != 'updated_at':
            setattr(get_city, k, v)
    storage.save()
    return jsonify(get_city.to_dict()), 200
