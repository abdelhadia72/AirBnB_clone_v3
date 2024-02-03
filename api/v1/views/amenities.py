#!/usr/bin/python3
""" Import the app_views blueprint for amenities API endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Get all amenity objects """
    all_amenities = storage.all("Amenity").values()
    list_amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>/',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Get an amenity by id """
    all_amenities = storage.all("Amenity").values()
    list_amenity = [amenity.to_dict() for amenity in all_amenities
                    if amenity.id == amenity_id]
    if not list_amenity:
        abort(404)
    return jsonify(list_amenity[0])


@app_views.route('/amenities/<amenity_id>/',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Remove an amenity by id """
    all_amenities = storage.all("Amenity").values()
    list_amenity = [amenity.to_dict() for amenity in
                    all_amenities if amenity.id == amenity_id]
    if not list_amenity:
        abort(404)
    list_amenity.remove(list_amenity[0])
    for amenity in all_amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Create a new amenity """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(name=request.json["name"])
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an amenity """
    all_amenities = storage.all("Amenity").values()
    amenity = [amenity.to_dict() for amenity in all_amenities
               if amenity_id == amenity.id]
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity[0]["name"] = request.get_json()["name"]
    for obj in all_amenities:
        if obj.id == amenity_id:
            obj.name = request.get_json()['name']
    storage.save()
    return jsonify(amenity[0]), 200
