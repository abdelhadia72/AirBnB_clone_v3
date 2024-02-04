#!/usr/bin/python3
"""
This file is the main entry point
for the AirBnB clone version 3 API.
"""


from api.v1.views import app_views
from os import getenv
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask import jsonify

app = Flask('__name__')
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def notFound(err):
    """ handler error 404 """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception=None):
    """ Close the database """
    storage.close()


if __name__ == "__main__":
    HBNB_HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    HBNB_PORT = getenv("HBNB_API_PORT", 5000)
    app.run(host=HBNB_HOST, port=HBNB_PORT, debug=True, threaded=True)
