import datetime
import requests
import sqlalchemy
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db, bp
from app.models import Doctor


auth_api = 'http://auth:5000'


def get_user_role():
    user_url = f'{auth_api}/get-user'
    user_response = requests.get(user_url, headers={'Authorization': request.headers['Authorization']})
    user = user_response.json()
    user_role = user['role']
    return user_role


def validate_create_data(data):
    mandatory_fields = ['firstName', 'lastName', 'specialty', 'dateOfBirth']
    missing_fields = [field for field in mandatory_fields if field not in data or data[field] == ""]
    if missing_fields:
        abort(400, description=f'Missing fields: {", ".join(missing_fields)}')


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


# -------------------------------------------------------------------------------------------------------------------- #


# Home
@bp.route('/', methods=['GET'])
def home():
    return jsonify(msg='Doctor service is up and running.'), 200


# Create a doctor profile
@bp.route('/create-doctor', methods=['POST'])
@jwt_required()
def create_doctor():
    data = request.get_json()
    user_id = get_jwt_identity()

    validate_create_data(data)

    user_role = get_user_role()

    if user_role != 'doctor':
        abort(403, description='User is not a doctor.')

    date_of_birth = datetime.datetime.strptime(data['dateOfBirth'], '%Y-%m-%dT%H:%M:%S.%fZ')

    new_doctor = Doctor(
        user_id=user_id,
        first_name=data['firstName'],
        last_name=data['lastName'],
        specialty=data['specialty'],
        date_of_birth=date_of_birth,
        address=data.get('address', None),
        phone_number=data.get('phoneNumber', None)
    )

    try:
        db.session.add(new_doctor)
        db.session.commit()

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        abort(500, description=f'An error occurred while creating the profile. {str(e)}')

    finally:
        db.session.close()

    return jsonify(msg='Profile created successfully.'), 201


# Update doctor information
@bp.route('/update-doctor', methods=['PUT'])
@jwt_required()
def update_doctor():
    user_id = get_jwt_identity()
    doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()
    data = request.get_json()

    validate_update_data(data, doctor, user_id)

    try:
        db.session.commit()

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        abort(500, description=f'An error occurred while updating the profile. {str(e)}')

    finally:
        db.session.close()

    return jsonify(msg='Doctor profile updated successfully!'), 200


# Delete a doctor profile
@bp.route('/delete-doctor', methods=['DELETE'])
@jwt_required()
def delete_profile():
    user_id = get_jwt_identity()
    doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()

    if not doctor:
        abort(404, description='Doctor not found.')

    if user_id != doctor.user_id:
        abort(403, description='User does not match token.')

    try:
        db.session.delete(doctor)
        db.session.commit()

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        abort(500, description=f'An error occurred while deleting the profile. {str(e)}')

    finally:
        db.session.close()

    return jsonify(msg='Doctor profile deleted successfully!'), 200


# Get the current doctor's profile
@bp.route('/get-doctor', methods=['GET'])
@jwt_required()
def get_doctor():
    user_id = get_jwt_identity()
    doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()

    if not doctor:
        abort(404, description='Doctor not found.')

    return jsonify({
        'id': doctor.id,
        'userId': doctor.user_id,
        'firstName': doctor.first_name,
        'lastName': doctor.last_name,
        'specialty': doctor.specialty,
        'dateOfBirth': doctor.date_of_birth,
        'address': doctor.address,
        'phoneNumber': doctor.phone_number
    }), 200


# Get doctor information by user ID
@bp.route('/get-doctor/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_doctor_by_user_id(user_id):
    doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()

    if not doctor:
        abort(404, description='Doctor not found.')

    return jsonify({
        'id': doctor.id,
        'firstName': doctor.first_name,
        'lastName': doctor.last_name,
        'specialty': doctor.specialty,
    }), 200


# Get doctor information by doctor ID
@bp.route('/get-doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    doctor = db.session.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        abort(404, description='Doctor not found.')

    return jsonify({
        'id': doctor.id,
        'firstName': doctor.first_name,
        'lastName': doctor.last_name,
        'specialty': doctor.specialty,
    }), 200


# Get all doctors
@bp.route('/get-doctors', methods=['GET'])
@jwt_required()
def get_all_doctors():
    doctors = db.session.query(Doctor).all()

    if not doctors:
        abort(404, description='No doctors found.')

    doctors_list = []
    for doctor in doctors:
        doctors_list.append({
            'id': doctor.id,
            'name': f'{doctor.first_name} {doctor.last_name}',
            'specialty': doctor.specialty,
        })

    return jsonify(doctors_list), 200
