import sqlalchemy
from flask import request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

from models import db, Doctor

# CORS
cors = CORS()

# JWT
jwt = JWTManager()


def data_create_check(data):
    if 'first_name' not in data or data['first_name'] == '':
        return jsonify(error='First name is required.'), 400

    if 'last_name' not in data or data['last_name'] == '':
        return jsonify(error='Last name is required.'), 400

    if 'date_of_birth' not in data or data['date_of_birth'] == '':
        return jsonify(error='Date of birth is required.'), 400

    if 'address' not in data or data['address'] == '':
        return jsonify(error='Address is required.'), 400

    return None


def data_update_check(data, doctor, user_id):
    if data is None:
        return jsonify(error='No data provided.'), 400

    if not doctor:
        return jsonify(error='Doctor not found.'), 404

    if user_id != doctor.user_id:
        return jsonify(error='User does not match token.'), 403

    if 'first_name' in data and data['first_name'] != '':
        doctor.first_name = data['first_name']

    if 'last_name' in data and data['last_name'] != '':
        doctor.last_name = data['last_name']

    if 'date_of_birth' in data and data['date_of_birth'] != '':
        doctor.date_of_birth = data['date_of_birth']

    if 'address' in data and data['address'] != '':
        doctor.address = data['address']

    if 'phone_number' in data and data['phone_number'] != '':
        doctor.phone_number = data['phone_number']


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
        user_id = get_jwt_identity()

        data_create_check(data)

        new_patient = Doctor(
            user_id=user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            address=data['address'],
            phone_number=data.get('phone_number', None)
        )

        try:
            db.session.add(new_patient)
            db.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            db.session.rollback()
            return jsonify(error=f'An error occurred while creating the profile. {str(e)}'), 500

        finally:
            db.session.close()

        return jsonify(msg='Profile created successfully.'), 200


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
            'user_id': doctor.user_id,
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
            'date_of_birth': doctor.date_of_birth,
            'address': doctor.address,
            'phone_number': doctor.phone_number
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
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
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
            'first_name': doctor.first_name,
            'last_name': doctor.last_name,
        }), 200
