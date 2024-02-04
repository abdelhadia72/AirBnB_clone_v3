#!/usr/bin/python3
"""review places"""

from flask import jsonify, request, abort, make_response
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews_placees(place_id):
    """ get the reviews by places """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def review(review_id):
    """return the review by his id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def add_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "user_id" not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_reviews(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return make_response("Not a JSON", 400)
    attributes = ["created_at", "updated_at", "id", "user_id",
                  "place_id"]
    for key, val in data.items():
        if key not in attributes:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
