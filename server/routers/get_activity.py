from flask import request, Blueprint, jsonify

from server.operators.db import get_activity

activities_api = Blueprint('activities_api', __name__)

@activities_api.route('/get_activity', methods=['GET'])
def get_activities():
    # # Extract query parameters
    # city = request.args.get('city')
    # start_date = request.args.get('start_date')
    # end_date = request.args.get('end_date')
    # is_physical = request.args.get('is_physical')
    # type_volunteer = request.args.get('type_volunteer')
    #
    # # Convert is_physical to a boolean if it's not None
    # if is_physical is not None:
    #     is_physical = True if is_physical.lower() == 'true' else False
    # Call the get_activity function with the parameters from the request
    activities = get_activity()
    columns = ['ActivityID', 'BusinessID', 'Date', 'IsPhysical', 'TypeVolunteer', 'ActivityDescription', 'VolunteersNeeded', 'City']

    # Convert tuples to dictionaries
    activities_list = [dict(zip(columns, activity)) for activity in activities]

    # Return the JSON response
    return jsonify(activities_list)
