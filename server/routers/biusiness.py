from flask import Blueprint, request, jsonify

# Assuming get_db_connection is defined somewhere in your application
from server.operators.db import create_business

# Blueprint setup
business_api = Blueprint('business_api', __name__)

# Create a route for adding a new business
@business_api.route('/create_business', methods=['POST'])
def add_business():
    data = request.get_json()

    # Extract data from the request
    business_name = data.get('business_name')
    city = data.get('city')
    user_id = data.get('user_id')

    # Validate the necessary information is provided
    if not all([business_name, city, user_id]):
        return jsonify({"message": "Missing data for business_name, city, or user_id"}), 400

    # Call the create_business function
    try:
        business_id, success = create_business(business_name, city, user_id)
        if success:
            return jsonify({"message": "Business successfully added", "business_id": business_id}), 201
        else:
            return jsonify({"message": "Failed to add business"}), 500
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"message": str(e)}), 500

# Add other routes and Flask app initialization as needed
