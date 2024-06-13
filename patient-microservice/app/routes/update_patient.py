import datetime
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, current_user


update_patient_bp = Blueprint('update_patient', __name__)


def update_data_check(data, patient, user_id):
    if data is None:
        abort(400, description='No data provided.')
    if not patient:
        abort(404, description='Patient not found.')
    if user_id != patient.user_id:
        abort(403, description='User does not match token.')
    if 'firstName' in data and data['firstName'] != '':
        patient.first_name = data['firstName']
    if 'lastName' in data and data['lastName'] != '':
        patient.last_name = data['lastName']
    if 'dateOfBirth' in data and data['dateOfBirth'] != '':
        date_of_birth = datetime.datetime.strptime(data['dateOfBirth'], '%Y-%m-%dT%H:%M:%S.%fZ')
        patient.date_of_birth = date_of_birth
    if 'address' in data and data['address'] != '':
        patient.address = data['address']
    if 'phoneNumber' in data and data['phoneNumber'] != '':
        patient.phone_number = data['phoneNumber']


# Update patient information
@update_patient_bp.route('/update-patient', methods=['PUT'])
@jwt_required()
def update_patient():
    data = request.get_json()

    update_data_check(data, current_user, current_user.user_id)
    current_user.save()

    return jsonify(msg='Patient profile updated successfully!'), 200
