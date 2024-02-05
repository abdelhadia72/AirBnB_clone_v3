#!/usr/bin/python3
"""App views for AirBnB_clone_v3

Indexing app views
"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
    Returns the status of the API.

    :return: A JSON object containing the status.
    """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def count():
    """
    Returns the number of each object by type.

    Returns:
        A JSON object containing the count of each object type.

    """
    alls = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for classx in classes:
        count = storage.count(classx)
        alls[classes.get(classx)] = count
    return jsonify(alls)
