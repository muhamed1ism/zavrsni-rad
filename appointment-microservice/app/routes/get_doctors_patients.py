from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required

from app.models.appointment import Appointment
from app.api.patient import get_patient_date_of_birth, get_patient_address, get_patient_phone_number
from app.api.doctor import get_doctor_id
from app import db

get_doctors_patients_bp = Blueprint('get_doctors_patients', __name__)


# Get doctor's patients from appointments where doctor id is equal to the doctor id of the current user
@get_doctors_patients_bp.route('/get-doctors-patients', methods=['GET'])
@jwt_required()
def get_doctors_patients():
    doctor_id = get_doctor_id()
    appointments = db.session.query(Appointment).filter(
        Appointment.doctor_id == doctor_id, Appointment.status == 'odobren'
    ).all()

    if not appointments:
        return jsonify(msg='No patients found.')

    patients_list = []
    for appointment in appointments:
        if any(d['id'] == appointment.patient_id for d in patients_list):
            continue
        date_of_birth = get_patient_date_of_birth(appointment.patient_id)
        address = get_patient_address(appointment.patient_id)
        phone_number = get_patient_phone_number(appointment.patient_id)
        patients_list.append({
            'id': appointment.patient_id,
            'name': appointment.patient_name,
            'dateOfBirth': date_of_birth,
            'address': address,
            'phoneNumber': phone_number
        })

    return jsonify(patients_list), 200
