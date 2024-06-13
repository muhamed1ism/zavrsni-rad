import os

from app.api.api_handler import api_request

api = os.getenv('API_ADDRESS_PATIENT', 'localhost:5001')


def get_patient():
    return api_request(api, 'get-patient', '')


def get_patient_by_patient_id(patient_id):
    return api_request(api, 'get-patient', patient_id)


def get_patient_id():
    patient = get_patient()
    patient_id = patient['id']
    return patient_id


def get_patient_name():
    patient = get_patient()
    patient_name = patient['firstName'] + ' ' + patient['lastName']
    return patient_name


def get_patient_address(patient_id):
    patient = get_patient_by_patient_id(patient_id)
    address = patient['address']
    return address


def get_patient_date_of_birth(patient_id):
    patient = get_patient_by_patient_id(patient_id)
    date_of_birth = patient['dateOfBirth']
    return date_of_birth


def get_patient_phone_number(patient_id):
    patient = get_patient_by_patient_id(patient_id)
    phone_number = patient['phoneNumber']
    return phone_number
