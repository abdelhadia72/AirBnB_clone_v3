#!/usr/bin/python3
"""
This file is the main entry point
for the AirBnB clone version 3 API.
"""

from api.v1.views import app_views
import os
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask('__name__')
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

if os.getenv("HBNB_API_HOST"):
    HBNB_HOST = os.getenv("HBNB_API_HOST")
else:
    HBNB_HOST = '0.0.0.0'

if os.getenv("HBNB_API_HOST"):
    HBNB_PORT = os.getenv("HBNB_API_PORT")
else:
    HBNB_PORT = 5000


@app.errorhandler(404)
def notFound(err):
    """ handler error 404 """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_db(exception=None):
    """ Close the database """
    storage.close()


if __name__ == "__main__":
    app.run(host=HBNB_HOST, port=HBNB_PORT, debug=True)
