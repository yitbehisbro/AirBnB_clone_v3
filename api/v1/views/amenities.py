#!/usr/bin/python3
""" Aminity view module """
from models.amenity import Amenity
from models import storage
from models.base_model import BaseModel
from api.v1.views.__init__ import app_views
from flask import jsonify
from flask import abort
from flask import request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def a_display():
    """ Retrieves the list of all 'class' objects """
    all_amenity = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in all_amenity.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def a_display_by_id(amenity_id):
    """ Retrieves the list of a class objects """
    get_amenity = storage.get(Amenity.__name__, amenity_id)
    if not get_amenity:
        abort(404)
    return jsonify(get_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def a_delete_by_id(amenity_id):
    """ Deletes a 'class' object """
    get_amenity = storage.get(Amenity.__name__, amenity_id)
    if not get_amenity:
        abort(404)
    get_amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def a_post_request():
    """ Posts a 'class' object """
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    if 'name' not in kwargs:
        abort(400, 'Missing name')

    get_amenity = Amenity(**kwargs)
    storage.new(get_amenity)
    storage.save()
    return jsonify(get_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def a_put_request(amenity_id):
    """ Puts a 'class' object """
    get_amenity = storage.get(Amenity.__name__, amenity_id)
    if not get_amenity:
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    for k, v in kwargs.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(get_amenity, k, v)
    storage.save()
    return jsonify(get_amenity.to_dict()), 200
