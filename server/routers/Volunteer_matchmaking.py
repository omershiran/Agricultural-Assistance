from flask import Blueprint, request, jsonify

from server.operators.db import make_match

# Blueprint setup
matching_api = Blueprint('matching_api', __name__)

@matching_api.route('/make_match', methods=['POST'])
def create_match():
    data = request.get_json()

    # Extract user_id and activity_id from the request data
    user_id = data.get('user_id')
    activity_id = data.get('activity_id')

    if not user_id or not activity_id:
        return jsonify({"message": "Missing user_id or activity_id"}), 400

    # Call the make_match function
    success = make_match(user_id, activity_id)

    # Return the appropriate response
    if success:
        return jsonify({"message": "Match successfully made"}), 201
    else:
        return jsonify({"message": "Failed to make match"}), 500

# Add other routes and Flask app initialization as needed
