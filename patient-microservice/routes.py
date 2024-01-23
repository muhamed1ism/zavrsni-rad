import sqlalchemy
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from models import db, Patient

# Flask
app = Flask(__name__)
# CORS
CORS(app)
# Config
app.config.from_object('config')
# Database
db.init_app(app)
# JWT
jwt = JWTManager(app)


# -------------------------------------------------------------------------------------- #


# Home route
@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the patient microservice!'


# Create profile route
@app.route('/profile/create', methods=['POST'])
@jwt_required()
def create_profile():
    try:
        user_id = get_jwt_identity()

        data = request.get_json()

        if 'first_name' not in data:
            return jsonify(error='First name is required.'), 400

        if 'last_name' not in data:
            return jsonify(error='Last name is required.'), 400

        if 'date_of_birth' not in data:
            return jsonify(error='Date of birth is required.'), 400

        if 'address' not in data:
            return jsonify(error='Address is required.'), 400

        new_patient = Patient(
            user_id=user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            address=data['address'],
            phone_number=data.get('phone_number', None)
        )

        db.session.add(new_patient)
        db.session.commit()

        return jsonify(msg='Profile created successfully.'), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred while creating the profile. {str(e)}'), 500

    finally:
        db.session.close()


# Get profile route
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()

        patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()

        if not patient:
            return jsonify(msg='Patient not found.'), 404

        return jsonify({
            'id': patient.id,
            'user_id': patient.user_id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'date_of_birth': patient.date_of_birth,
            'address': patient.address,
            'phone_number': patient.phone_number
        }), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        return jsonify(error=f'An error occurred while retrieving the profile. {str(e)}'), 500

    finally:
        db.session.close()


# Update profile route
@app.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()

        if not patient:
            return jsonify(error='Patient not found.'), 404

        data = request.get_json()

        if data is None:
            return jsonify(error='No data provided.'), 400

        if user_id != patient.user_id:
            return jsonify(error='User does not match token.'), 403

        if 'first_name' in data:
            patient.first_name = data['first_name']

        if 'last_name' in data:
            patient.last_name = data['last_name']

        if 'date_of_birth' in data:
            patient.date_of_birth = data['date_of_birth']

        if 'address' in data:
            patient.address = data['address']

        if 'phone_number' in data:
            patient.phone_number = data['phone_number']

        db.session.commit()

        return jsonify(msg='Patient profile updated successfully!'), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred while updating the profile. {str(e)}'), 500

    finally:
        db.session.close()


# Delete profile route
@app.route('/profile/delete', methods=['DELETE'])
@jwt_required()
def delete_profile():
    try:
        user_id = get_jwt_identity()

        patient = db.session.query(Patient).filter(Patient.user_id == user_id).first()

        if not patient:
            return jsonify(error='Patient not found.'), 404

        if user_id != patient.user_id:
            return jsonify(error='User does not match token.'), 403

        db.session.delete(patient)
        db.session.commit()

        return jsonify(msg='Patient profile deleted successfully!'), 200

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred while deleting the profile. {str(e)}'), 500

    finally:
        db.session.close()
