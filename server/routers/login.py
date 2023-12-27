from flask import Blueprint, request, jsonify


from server.operators.db import get_db_connection, get_user

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    # Extract email and password from the request
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Attempt to retrieve the user from the database
    success, user_id, business_id = get_user(email, password)

    # Check the success and respond accordingly
    if success:
        return jsonify({"message": "Login successful", "user_id": user_id, "business_id": business_id}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# Add other routes and Flask app initialization as needed
