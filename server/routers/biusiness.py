from flask import Flask, request,jsonify, Blueprint
from operators.db import is_business_exist, create_business

import json
import operators.db as db

app = Flask(__name__)
business_api = Blueprint('business_api', __name__)

@business_api.route('/register_business', methods=['POST'])
def register_business():
    req_data = request.get_json()
    business_name = req_data.get('business_name')
    city = req_data.get('city')
    user_id = req_data.get('user_id')

    response = is_business_exist(user_id,business_name)  # Assuming user_id is used to check user existence

    if len(response) == 1:  # Assuming user_id should return only one user
        # Successful business registration
        try:
            # Add the business with provided details and user_id
            business_id = create_business(business_name, city, user_id)
            return jsonify({'business_id': business_id}), 200
        except Exception as e:
            print('Error:', e)
            return jsonify({'message': 'Error occurred while registering business'}), 500
    else:
        # Invalid user ID
        return jsonify({'message': 'Invalid user ID'}), 400

if __name__ == '__main__':
    app.run(debug=True)