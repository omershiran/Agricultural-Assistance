from flask import Blueprint, request
import json
import operators.db as db
# import sys
# sys.path.append('../')

# registration_api = Blueprint('registration_api', __name__)



# @registration_api.route('/registration', methods=['POST'])
# def registration():
#     pass
from flask import Flask, request, jsonify
from operators.db import add_user, check_mail

app = Flask(__name__)

# Assuming dbBridge is a module with functions addUser and getUser

# POST register section
registration_api = Blueprint('registration_api', __name__)

registration_api()

@registration_api.route('/register', methods=['POST'])
def registration_api():
    req_data = request.get_json()
    first_name = 'yehuda'
    # req_data.get('first_name')
    last_name = 'm'
    # req_data.get('last_name')
    email = '@'
    # req_data.get('email')
    password = '13' 
    # req_data.get('password')
    phone_number = '111'
    # req_data.get('phone_number')

    response = check_mail(email)

    if response == False:
        # Successful register
        try:
            add_user(first_name,last_name,email,password,phone_number)
            return jsonify({'message': 'Register successful'}), 200
        except Exception as e:
            print('Error:', e)
            return jsonify({'message': 'Error occurred'}), 401
    else:
        # Username taken
        return jsonify({'message': 'Username taken'}), 401

if __name__ == '__main__':
    app.run(debug=True)