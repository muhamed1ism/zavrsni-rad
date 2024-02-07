import datetime
import requests
import sqlalchemy
from flask import request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

from models import db, Doctor

# CORS
cors = CORS()
# JWT
jwt = JWTManager()

auth_url = 'http://auth:5000'


def get_user_role():
    user_url = f'{auth_url}/get-user'
    user_response = requests.get(user_url, headers={'Authorization': request.headers['Authorization']})
    user = user_response.json()
    user_role = user['role']
    return user_role


def data_create_check(data):
    mandatory_fields = ['firstName', 'lastName', 'specialty', 'dateOfBirth']
    missing_fields = [field for field in mandatory_fields if field not in data or data[field] == ""]
    if missing_fields:
        return jsonify(error=f'{", ".join(missing_fields)} are required.'), 400


def data_update_check(data, doctor, user_id):
    if data is None:
        return jsonify(error='No data provided.'), 400
    if not doctor:
        return jsonify(error='Doctor not found.'), 404
    if user_id != doctor.user_id:
        return jsonify(error='User does not match token.'), 403
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


def app_routes(app):
    app_route_home(app)
    app_route_create_doctor(app)
    app_route_update_doctor(app)
    app_route_delete_doctor(app)
    app_route_get_doctor(app)
    app_route_get_all_doctors(app)
    app_route_get_doctor_by_id(app)
    app_route_get_doctor_by_user_id(app)


# -------------------------------------------------------------------------------------------------------------------- #


# Home
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
            'specialty': doctor.specialty,
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
            'specialty': doctor.specialty,
        }), 200


# Get doctor information by doctor ID
def app_route_get_doctor_by_id(app):

    @app.route('/get-doctor/<int:doctor_id>', methods=['GET'])
    def get_doctor_by_id(doctor_id):
        doctor = db.session.query(Doctor).filter(Doctor.id == doctor_id).first()

        if not doctor:
            return jsonify(msg='Doctor not found.'), 404

        return jsonify({
            'id': doctor.id,
            'firstName': doctor.first_name,
            'lastName': doctor.last_name,
            'specialty': doctor.specialty,
        }), 200

# Get all doctors
def app_route_get_all_doctors(app):

    @app.route('/get-doctors', methods=['GET'])
    @jwt_required()
    def get_all_doctors():
        doctors = db.session.query(Doctor).all()

        if not doctors:
            return jsonify(msg='No doctors found.'), 404

        doctors_list = []
        for doctor in doctors:
            doctors_list.append({
                'id': doctor.id,
                'name': f'{doctor.first_name} {doctor.last_name}',
                'specialty': doctor.specialty,
            })

        return jsonify(doctors_list), 200
