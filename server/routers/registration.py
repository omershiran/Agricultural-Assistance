from flask import Blueprint, request, jsonify
import sqlite3
# Import a password hashing library - ensure to install it first
from werkzeug.security import generate_password_hash

from server.operators.db import get_db_connection, add_user


user_api = Blueprint('user_api', __name__)

@user_api.route('/register', methods=['POST'])

def register_user():
    data = request.get_json()

    # Extract data from the request
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')
    # Validate that all required data is provided
    if not all([first_name, last_name, email, password, phone_number]):
        return jsonify({"message": "All fields are required"}), 400


    # Attempt to register the user
    try:
        success, user_id = add_user(first_name, last_name, email, password, phone_number)
        if success:
            return jsonify({"message": "Registration successful", "user_id": user_id}), 201
        else:
            # Provide a more specific message in a real-world scenario
            return jsonify({"message": "Registration failed"}), 500
    except sqlite3.IntegrityError:
        # This typically occurs if the email is already in use
        return jsonify({"message": "This email is already registered"}), 400
    except Exception as e:
        # Log the error for debugging
        print(f"An unexpected error occurred: {e}")
        return jsonify({"message": "An error occurred during registration"}), 500

# Add other routes and Flask app initialization as needed
