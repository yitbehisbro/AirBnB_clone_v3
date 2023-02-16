#!/usr/bin/python3
""" Aminity view module """
from models.user import User
from models import storage
from models.base_model import BaseModel
from api.v1.views.__init__ import app_views
from flask import jsonify
from flask import abort
from flask import request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def u_display():
    """ Retrieves the list of all 'class' objects """
    all_user = storage.all(User)
    return jsonify([user.to_dict() for user in all_user.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def u_display_by_id(user_id):
    """ Retrieves the list of a class objects """
    get_user = storage.get(User.__name__, user_id)
    if not get_user:
        abort(404)
    return jsonify(get_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def u_delete_by_id(user_id):
    """ Deletes a 'class' object """
    get_user = storage.get(User.__name__, user_id)
    if not get_user:
        abort(404)
    get_user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def u_post_request():
    """ Posts a 'class' object """
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    if 'email' not in kwargs:
        abort(400, 'Missing email')
    if 'password' not in kwargs:
        abort(400, 'Missing password')
    get_user = User(**kwargs)
    storage.new(get_user)
    storage.save()
    return jsonify(get_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def u_put_request(user_id):
    """ Puts a 'class' object """
    get_user = storage.get(User.__name__, user_id)
    if not get_user:
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    for k, v in kwargs.items():
        if k != 'id' and k != email and k != 'created_at' and k != 'updated_at':
            setattr(get_user, k, v)
    storage.save()
    return jsonify(get_user.to_dict()), 200
