from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Location, SavedLocation, location_schema, location_multi_schema, user_schema

api = Blueprint('ap', __name__, url_prefix='/api')

# Get all locations saved by user
@api.route('/location', methods = ['GET'])
@token_required
def get_locations(current_user_token):
    user_token = current_user_token.token
    locations = SavedLocation.query.filter_by(user_token=user_token).all()
    if locations:
        response = location_multi_schema.dump(locations)
        return jsonify(response)
    return jsonify({'message' : 'Item not found'}), 404

# Save new location
@api.route('/location', methods = ['POST'])
@token_required
def add_location(current_user_token):
    name = request.json['name']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    timezone = request.json['timezone']
    location_api_id = request.json['location_api_id']
    user_token = current_user_token.token

    try:
        location = Location(name, latitude, longitude, timezone, location_api_id)
        db.session.add(location)
        db.session.commit()

        location_to_save = Location.query.filter_by(location_api_id=location_api_id).all()
        saved = SavedLocation(user_token, location_to_save[0].id)
        db.session.add(saved)
        db.session.commit()

        response = location_schema.dump(location)
        return jsonify(response)
    except:
        return jsonify({'message' : 'Failed to add item'}), 500

# Delete saved location
@api.route('/location/<location_id>', methods = ['DELETE'])
@token_required
def delete_location(current_user_token, location_id):
    user_token = current_user_token.token
    saved = SavedLocation.query.filter_by(user_token=user_token, location_id=location_id).all()
    if saved:
        db.session.delete(saved)
        db.session.commit()
        response = location_schema.dump(saved)
        return jsonify(response)
    return jsonify({'message' : 'Item not found'}), 404
    
# Update user info
@api.route('/user/<user_id>', methods = ['POST','PUT'])
@token_required
def update_user(current_user_token, user_id):
    user_token = current_user_token.token
    user = User.query.get(user_id)
    if user and user.user_token == user_token:
        user.first_name = request.json['first_name']
        db.session.commit()
        response = user_schema.dump(user)
        return jsonify(response)
    return jsonify({'message' : 'User not found'}), 404