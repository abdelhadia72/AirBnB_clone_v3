#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def list_states():
    '''GET all State'''
    states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''GET State '''
    all_states = storage.all("State").values()
    states = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if states == []:
        abort(404)
    return jsonify(states[0])


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''DELETE State'''
    all_states = storage.all("State").values()
    states = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if states == []:
        abort(404)
    states.remove(states[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    '''POST a State'''
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updates_state(state_id):
    '''Updates a State object'''
    all_states = storage.all("State").values()
    states = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if states == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    states[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(states[0]), 200
