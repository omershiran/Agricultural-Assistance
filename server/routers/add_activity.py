from flask import Blueprint, request, jsonify
import json



import sys
sys.path.append('../')
from operators.db import create_activity


add_activity_api = Blueprint('add_activity_api', __name__)

@add_activity_api.route('/add_activity', methods=['POST'])
def add_activity():
    # Extract data from the request
    data = request.get_json()
    BusinessID = data.get('BusinessID')
    date = data.get('date')
    is_physical = data.get('is_physical')
    NumberOfVolunteers = data.get('NumberOfVolunteers')
    type_volunteer = data.get('type_volunteer')
    ActivityDescription = data.get('ActivityDescription')

    # Call the create_activity function with data from request
    success = create_activity(BusinessID, date, is_physical, NumberOfVolunteers, type_volunteer, ActivityDescription)

    # Return a response based on the success of the create_activity function
    if success:
        return jsonify({"message": "Activity successfully added"}), 201
    else:
        return jsonify({"message": "Failed to add activity"}), 500
