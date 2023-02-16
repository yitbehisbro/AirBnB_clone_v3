#!/usr/bin/python3
""" Place review view module """
from models.place import Place
from models.city import City
from models.review import Review
from models import storage
from api.v1.views.__init__ import app_views
from flask import jsonify
from flask import abort
from flask import request

from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def pr_display(place_id):
    """ Retrieves the list of a class objects """
    get_place = storage.get(Place.__name__, place_id)
    if not get_place:
        abort(404)
    return jsonify([place.to_dict() for place in get_place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def pr_display_by_id(review_id):
    """ Retrieves the list of a class objects """
    review = storage.get(Review.__name__, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def pr_delete_by_id(review_id):
    """ Deletes a 'class' object """
    review = storage.get(Review.__name__, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def pr_post_request(place_id):
    """ Posts a 'class' object """
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    if 'text' not in kwargs:
        abort(400, 'Missing text')
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')
    user_id = kwargs['user_id']
    if not storage.get(User.__name__, user_id):
        abort(404)
    reviews = Review(**kwargs)
    setattr(reviews, 'place_id', place_id)
    storage.new(reviews)
    storage.save()
    return jsonify(reviews.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def pr_put_request(review_id):
    """ Puts a 'class' object """
    get_reviews = storage.get(Review.__name__, review_id)
    if not get_reviews:
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    review = kwargs['review_id']
    if review not in storage.get(Review.__name__, review_id):
        abort(404)
    for k, v in kwargs.items():
        if k != 'id' and k != 'user_id' and k != 'place_id'\
                and k != 'created_at' and k != 'updated_at':
            setattr(get_reviews, k, v)
    storage.save()
    return jsonify(get_reviews.to_dict()), 200
