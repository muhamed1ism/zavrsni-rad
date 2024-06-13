import datetime
from flask import request, jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.auth import get_user_role
from app.models.patient import Patient

create_patient_bp = Blueprint('create_patient', __name__)


def validate_create_data(data, user_role):
    mandatory_fields = ['firstName', 'lastName', 'dateOfBirth']
    missing_fields = [field for field in mandatory_fields if not (field in data and data[field].strip())]
    if missing_fields:
        abort(400, description=f'Missing fields: {", ".join(missing_fields)}')
    if user_role != 'patient':
        abort(403, description='User is not a patient.')


# Create a patient profile
@create_patient_bp.route('/create-patient', methods=['POST'])
@jwt_required()
def create_patient():
    data = request.get_json()
    user_role = get_user_role()

    validate_create_data(data, user_role)

    date_of_birth = datetime.datetime.strptime(data.get('dateOfBirth'), '%Y-%m-%dT%H:%M:%S.%fZ')

    new_patient = Patient(
        user_id=get_jwt_identity(),
        first_name=data.get('firstName'),
        last_name=data.get('lastName'),
        date_of_birth=date_of_birth,
        address=data.get('address'),
        phone_number=data.get('phoneNumber')
    )
    new_patient.save()

    return jsonify(msg='Profile created successfully.'), 201
