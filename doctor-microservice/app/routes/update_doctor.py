import datetime
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, current_user

update_doctor_bp = Blueprint('update_doctor', __name__)


def validate_update_data(data, doctor, user_id):
    if data is None:
        abort(400, description='No data provided.')
    if not doctor:
        abort(404, description='Doctor not found.')
    if user_id != doctor.user_id:
        abort(403, description='User does not match token.')
    if 'firstName' in data and data['firstName'] != "":
        doctor.first_name = data['firstName']
    if 'lastName' in data and data['lastName'] != "":
        doctor.last_name = data['lastName']
    if 'specialty' in data and data['specialty'] != "":
        doctor.specialty = data['specialty']
    if 'address' in data and data['address'] != "":
        doctor.address = data['address']
    if 'phoneNumber' in data and data['phoneNumber'] != "":
        doctor.phone_number = data['phoneNumber']
    if 'dateOfBirth' in data and data['dateOfBirth'] != "":
        date_of_birth = datetime.datetime.strptime(data['dateOfBirth'], '%Y-%m-%dT%H:%M:%S.%fZ')
        doctor.date_of_birth = date_of_birth


# Update doctor information
@update_doctor_bp.route('/update-doctor', methods=['PUT'])
@jwt_required()
def update_doctor():
    data = request.get_json()

    validate_update_data(data, current_user, current_user.user_id)
    current_user.save()

    return jsonify(msg='Doctor profile updated successfully!'), 200
