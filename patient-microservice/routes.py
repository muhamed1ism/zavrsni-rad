import requests
from flask import Flask, request, jsonify
from models import db, Patient
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

auth_microservice_url = 'http://localhost:5000'


@app.get('/')
def home():
    return 'Welcome to the patient microservice!'


@app.post('/create-patient/<int:user_id>')
def create_patient(user_id):
    auth_check_user_url = f'{auth_microservice_url}/check-user/{user_id}'

    response = requests.get(auth_check_user_url)

    if response.status_code != 200:
        return jsonify({'message': 'User does not exist.', 'status': 'danger'})

    user_exists = response.json()['user_exists']

    if not user_exists:
        return jsonify({'message': 'User does not exist.', 'status': 'danger'})

    data = request.get_json()

    new_patient = Patient(
        user_id=user_id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=data['date_of_birth'],
        address=data['address'],
        phone_number=data['phone_number']
    )
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient created successfully!', 'status': 'success'})


@app.post('/update-patient/<int:user_id>')
def update_patient(user_id):
    auth_check_user_url = f'{auth_microservice_url}/check-user/{user_id}'

    response = requests.get(auth_check_user_url)

    if response.status_code != 200:
        return jsonify({'message': 'User does not exist.', 'status': 'danger'})

    user_exists = response.json()['user_exists']

    if not user_exists:
        return jsonify({'message': 'User does not exist.', 'status': 'danger'})

    data = request.get_json()

    patient = db.session.query(Patient).filter_by(user_id=user_id).first()

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

    patient.updated_at = datetime.now()

    db.session.commit()

    return jsonify({'message': 'Patient updated successfully!', 'status': 'success'})


@app.post('/delete-patient/<int:user_id>')
def delete_patient(user_id):
    auth_check_user_url = f'{auth_microservice_url}/check-user/{user_id}'

    response = requests.get(auth_check_user_url)

    if response.status_code != 200:
        return jsonify({'message': 'User does not exist.', 'status': 'danger'})

    user_exists = response.json()['user_exists']

    if not user_exists:
        return jsonify({'message': 'User does not exist.', 'status': 'danger'})

    patient = db.session.query(Patient).filter_by(user_id=user_id).first()

    db.session.delete(patient)
    db.session.commit()

    return jsonify({'message': 'Patient deleted successfully!', 'status': 'success'})

