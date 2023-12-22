from flask import Blueprint, request
import json
import operators.db as db
# import sys
# sys.path.append('../')

registration_api = Blueprint('registration_api', __name__)



@registration_api.route('/registration', methods=['POST'])
def registration():
    pass