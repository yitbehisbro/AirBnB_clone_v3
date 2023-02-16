#!/usr/bin/python3
""" State view module """
from models.state import State
from models import storage
from models.base_model import BaseModel
from api.v1.views.__init__ import app_views
from flask import jsonify
from flask import abort
from flask import request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def display():
    """ Retrieves the list of all 'class' objects """
    all_state = storage.all(State)
    return jsonify([state.to_dict() for state in all_state.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def display_by_id(state_id):
    """ Retrieves the list of a class objects """
    get_state = storage.get(State.__name__, state_id)
    if not get_state:
        abort(404)
    return jsonify(get_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_by_id(state_id):
    """ Deletes a 'class' object """
    get_state = storage.get(State.__name__, state_id)
    if not get_state:
        abort(404)
    get_state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_request():
    """ Posts a 'class' object """
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    if 'name' not in kwargs:
        abort(400, 'Missing name')

    get_state = State(**kwargs)
    storage.new(get_state)
    storage.save()
    return jsonify(get_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_request(state_id):
    """ Puts a 'class' object """
    get_state = storage.get(State.__name__, state_id)
    if not get_state:
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    for k, v in kwargs.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(get_state, k, v)
    storage.save()
    return jsonify(get_state.to_dict()), 200
