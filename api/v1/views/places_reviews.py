#!/usr/bin/python3
"""review places"""

from flask import jsonify, request, abort, make_response
from models.place import Place
from models.review import Review
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


