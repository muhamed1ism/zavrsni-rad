import os

from app.api.api_handler import api_request

api = os.getenv('API_ADDRESS_DOCTOR', 'localhost:5002')


def get_doctor():
    return api_request(api, 'get-doctor/user', '')


def get_doctor_by_doctor_id(doctor_id):
    return api_request(api, 'get-doctor', doctor_id)


def get_doctor_id():
    doctor = get_doctor()
    doctor_id = doctor['id']
    return doctor_id


def get_doctor_name(doctor_id):
    doctor = get_doctor_by_doctor_id(doctor_id)
    doctor_name = doctor['firstName'] + ' ' + doctor['lastName']
    return doctor_name
