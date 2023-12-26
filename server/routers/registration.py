# from flask import Blueprint, request
# import json
# import operators.db as db
# # import sys
# # sys.path.append('../')

# registration_api = Blueprint('registration_api', __name__)



# @registration_api.route('/registration', methods=['POST'])
# def registration():
#     pass
from flask import Flask, request, jsonify
from operators.db import add_user, check_mail

app = Flask(__name__)

# Assuming dbBridge is a module with functions addUser and getUser

# POST register section
@app.route('/', methods=['POST'])
def registration_api():
    req_data = request.get_json()
    mail = req_data.get('email')

    response = check_mail(mail)

    if response == False:
        # Successful register
        try:
            add_user(req_data)
            return jsonify({'message': 'Register successful'}), 200
        except Exception as e:
            print('Error:', e)
            return jsonify({'message': 'Error occurred'}), 401
    else:
        # Username taken
        return jsonify({'message': 'Username taken'}), 401

if __name__ == '__main__':
    app.run(debug=True)