import datetime
import requests
import sqlalchemy
from flask import request, jsonify, abort
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

from app.models import db, Patient

# CORS
cors = CORS()
# JWT
jwt = JWTManager()

auth_api = 'http://auth:5000'


def get_user_role():
    user_url = f'{auth_api}/get-user'
    user_response = requests.get(user_url, headers={'Authorization': request.headers['Authorization']})
    user = user_response.json()
    user_role = user['role']
    return user_role


def create_data_check(data):
    if 'firstName' not in data or data['firstName'] == '':
        abort(400, description='First name is required.')
    if 'lastName' not in data or data['lastName'] == '':
        abort(400, description='Last name is required.')
    if 'dateOfBirth' not in data or data['dateOfBirth'] == '':
        abort(400, description='Date of birth is required.')

    return None


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

    return None


def app_routes(app):
    app_route_home(app)
    app_route_create_patient(app)
    app_route_update_patient(app)
    app_route_delete_patient(app)
    app_route_get_patient(app)
    app_route_get_patient_by_id(app)
    app_route_get_patient_by_user_id(app)


# -------------------------------------------------------------------------------------------------------------------- #


# Home
def app_route_home(app):
    @app.route('/', methods=['GET'])
    def home():
        return jsonify(msg='Patient service is up and running.'), 200


# Create a patient profile
def app_route_create_patient(app):
    @app.route('/create-patient', methods=['POST'])
    @jwt_required()
    def create_patient():
        data = request.get_json()
        user_id = get_jwt_identity()

        create_data_check(data)

        user_role = get_user_role()

        if user_role != 'patient':
            abort(403, description='User is not a patient.')

        date_of_birth = datetime.datetime.strptime(data['dateOfBirth'], '%Y-%m-%dT%H:%M:%S.%fZ')

        new_patient = Patient(
            user_id=user_id,
            first_name=data['firstName'],
            last_name=data['lastName'],
            date_of_birth=date_of_birth,
            address=data.get('address', None),
            phone_number=data.get('phoneNumber', None)
        )

        try:
            db.session.add(new_patient)
            db.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
            abort(500, description=f'An error occurred while creating the profile. {str(e)}')

        finally:
            db.session.close()

        return jsonify(msg='Profile created successfully.'), 201


# Update patient information
def app_route_update_patient(app):
    @app.route('/update-patient', methods=['PUT'])
    @jwt_required()
    def update_patient():
        data = request.get_json()
        user_id = get_jwt_identity()
        patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()

        update_data_check(data, patient, user_id)

        try:
            db.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
            abort(500, description=f'An error occurred while updating the profile. {str(e)}')

        finally:
            db.session.close()

        return jsonify(msg='Patient profile updated successfully!'), 200


# Delete a patient profile
def app_route_delete_patient(app):
    @app.route('/delete-patient', methods=['DELETE'])
    @jwt_required()
    def delete_patient():
        user_id = get_jwt_identity()
        patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()

        if not patient:
            abort(404, description='Patient not found.')

        if user_id != patient.user_id:
            abort(403, description='User does not match token.')

        try:
            db.session.delete(patient)
            db.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
            abort(500, description=f'An error occurred while deleting the profile. {str(e)}')

        finally:
            db.session.close()

        return jsonify(msg='Patient profile deleted successfully!'), 200


# Get the current patient's profile
def app_route_get_patient(app):
    @app.route('/get-patient', methods=['GET'])
    @jwt_required()
    def get_patient():
        user_id = get_jwt_identity()
        patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()

        if not patient:
            abort(404, description='Patient not found.')

        patient_data = {
            'id': patient.id,
            'userId': patient.user_id,
            'firstName': patient.first_name,
            'lastName': patient.last_name,
            'dateOfBirth': patient.date_of_birth,
            'address': patient.address,
            'phoneNumber': patient.phone_number
        }

        return jsonify(patient_data), 200


# Get patient information by patient ID
def app_route_get_patient_by_id(app):
    @app.route('/get-patient/<int:patient_id>', methods=['GET'])
    @jwt_required()
    def get_patient_by_id(patient_id):
        patient = db.session.query(Patient).filter(Patient.id == patient_id).first()

        if not patient:
            abort(404, description='Patient not found.')

        patient_data = {
            'id': patient.id,
            'userId': patient.user_id,
            'firstName': patient.first_name,
            'lastName': patient.last_name,
            'dateOfBirth': patient.date_of_birth,
            'address': patient.address,
            'phoneNumber': patient.phone_number
        }

        return jsonify(patient_data), 200


# Get patient information by user ID
def app_route_get_patient_by_user_id(app):
    @app.route('/get-patient/user/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_patient_by_user_id(user_id):
        patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()

        if not patient:
            abort(404, description='Patient not found.')

        patient_data = {
            'id': patient.id,
            'userId': patient.user_id,
            'firstName': patient.first_name,
            'lastName': patient.last_name,
            'dateOfBirth': patient.date_of_birth,
            'address': patient.address,
            'phoneNumber': patient.phone_number
        }

        return jsonify(patient_data), 200
