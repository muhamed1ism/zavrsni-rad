import requests
import sqlalchemy
from flask import request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

from models import db, Doctor

# CORS
CORS_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5000',
    'http://localhost:5001',
    'http://localhost:5003'
]
cors = CORS(origins=CORS_ORIGINS)
# JWT
jwt = JWTManager()


def get_user_role():
    user_url = 'http://localhost:5000/get-user'
    user_response = requests.get(user_url, headers={'Authorization': request.headers['Authorization']})
    user = user_response.json()
    user_role = user['role']
    return user_role


def data_create_check(data):
    mandatory_fields = ['firstName', 'lastName', 'dateOfBirth']
    missing_fields = [field for field in mandatory_fields if field not in data or data[field] == ""]
    if missing_fields:
        return jsonify(error=f'{", ".join(missing_fields)} are required.'), 400


def update_doctor_data(doctor, data, fields):
    for field in fields:
        if field in data and data[field] != '':
            setattr(doctor, field, data[field])


def data_update_check(data, doctor, user_id):
    if data is None:
        return jsonify(error='No data provided.'), 400
    if not doctor:
        return jsonify(error='Doctor not found.'), 404
    if user_id != doctor.user_id:
        return jsonify(error='User does not match token.'), 403
    update_doctor_data(doctor, data, ['firstName', 'lastName', 'dateOfBirth', 'address', 'phoneNumber'])


def app_routes(app):
    app_route_home(app)
    app_route_create_doctor(app)
    app_route_update_doctor(app)
    app_route_delete_doctor(app)
    app_route_get_doctor(app)
    app_route_get_doctor_by_id(app)
    app_route_get_doctor_by_user_id(app)


# -------------------------------------------------------------------------------------------------------------------- #


# Home route
def app_route_home(app):

    @app.route('/', methods=['GET'])
    def home():
        return jsonify(msg='Doctor service is up and running.'), 200


# Create a doctor profile
def app_route_create_doctor(app):

    @app.route('/create-doctor', methods=['POST'])
    @jwt_required()
    def create_doctor():
        data = request.get_json()
        missing = data_create_check(data)
        if missing:
            return missing
        user_id = get_jwt_identity()

        user_role = get_user_role()

        if user_role != 'doctor':
            return jsonify(error='User is not a doctor.'), 403

        new_patient = Doctor(
            user_id=user_id,
            first_name=data['firstName'],
            last_name=data['lastName'],
            date_of_birth=data['dateOfBirth'],
            address=data.get('address', None),
            phone_number=data.get('phoneNumber', None)
        )

        try:
            db.session.add(new_patient)
            db.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify(error=f'An error occurred while creating the profile. {str(e)}'), 500

        finally:
            db.session.close()

        return jsonify(msg='Profile created successfully.'), 201


# Update doctor information
def app_route_update_doctor(app):

    @app.route('/update-doctor', methods=['PUT'])
    @jwt_required()
    def update_doctor():
        user_id = get_jwt_identity()
        doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()
        data = request.get_json()

        data_update_check(data, doctor, user_id)

        try:
            db.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify(error=f'An error occurred while updating the profile. {str(e)}'), 500

        finally:
            db.session.close()

        return jsonify(msg='Doctor profile updated successfully!'), 200


# Delete a doctor profile
def app_route_delete_doctor(app):

    @app.route('/delete-doctor', methods=['DELETE'])
    @jwt_required()
    def delete_profile():
        user_id = get_jwt_identity()
        doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()

        if not doctor:
            return jsonify(error='Doctor not found.'), 404

        if user_id != doctor.user_id:
            return jsonify(error='User does not match token.'), 403

        try:
            db.session.delete(doctor)
            db.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify(error=f'An error occurred while deleting the profile. {str(e)}'), 500

        finally:
            db.session.close()

        return jsonify(msg='Doctor profile deleted successfully!'), 200


# Get the current doctor's profile
def app_route_get_doctor(app):

    @app.route('/get-doctor', methods=['GET'])
    @jwt_required()
    def get_doctor():
        user_id = get_jwt_identity()
        doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()

        if not doctor:
            return jsonify(msg='Doctor not found.'), 404

        return jsonify({
            'id': doctor.id,
            'userId': doctor.user_id,
            'firstName': doctor.first_name,
            'lastName': doctor.last_name,
            'dateOfBirth': doctor.date_of_birth,
            'address': doctor.address,
            'phoneNumber': doctor.phone_number
        }), 200


# Get doctor information by user ID
def app_route_get_doctor_by_user_id(app):

    @app.route('/get-doctor/user/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_doctor_by_user_id(user_id):
        doctor = db.session.query(Doctor).filter(Doctor.user_id == user_id).first()

        if not doctor:
            return jsonify(msg='Doctor not found.'), 404

        return jsonify({
            'id': doctor.id,
            'firstName': doctor.first_name,
            'lastName': doctor.last_name,
        }), 200


# Get doctor information by doctor ID
def app_route_get_doctor_by_id(app):

    @app.route('/get-doctor/<int:doctor_id>', methods=['GET'])
    def get_doctor_by_id(doctor_id):
        doctor = db.session.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()

        if not doctor:
            return jsonify(msg='Doctor not found.'), 404

        return jsonify({
            'id': doctor.id,
            'firstName': doctor.first_name,
            'lastName': doctor.last_name,
        }), 200
