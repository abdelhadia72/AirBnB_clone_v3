#!/usr/bin/python3
"""Amenity objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
import os

'''
Here what I did I get the Place by it's id and 
then I look to the list in that palce named amenity_ids
that hold all ids of amenitys and I start geting all amenitys 
and return them into a list and return it as a json object
'''
@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [storage.get(Amenity, id).to_dict() for id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_(place_id, amenity_id):
    """Deletes a Amenity object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity_id not in place.amenity_ids:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
        amenity_to_delete = storage.get(Amenity, amenity_id)
        storage.delete(amenity_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity_by_place_(place_id):
    """Creates a Amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data = request.get_json()
    amenity = Amenity(**data)
    amenity.save()
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_place_(place_id, amenity_id):
    """Deletes a Amenity object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200



