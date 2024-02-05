#!/usr/bin/python3
"""index file"""

from flask import jsonify
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


all_classess = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """test status OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """return the count of all objects"""
    new_classes = {}
    for key, value in all_classess.items():
        new_classes[key] = storage.count(value)
    return jsonify(new_classes)
