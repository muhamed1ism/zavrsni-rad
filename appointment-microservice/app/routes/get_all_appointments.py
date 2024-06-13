from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required

from app.models.appointment import Appointment
from app.api.patient import get_patient_id
from app.api.doctor import get_doctor_id
from app.api.auth import get_user_role

get_all_appointments_bp = Blueprint('get_all_appointments', __name__)


# Get all user appointments based on user role
@get_all_appointments_bp.route('/get-all-appointments', methods=['GET'])
@jwt_required()
def get_all_appointments():
    user_role = get_user_role()

    id = get_patient_id() if user_role == 'patient' else get_doctor_id()

    appointments = Appointment.query.filter_by(patient_id=id) if user_role == 'patient' \
        else Appointment.query.filter_by(doctor_id=id)

    if not appointments:
        return jsonify(msg='No appointments found.')

    appointments_list = [{
        'id': appointment.id,
        'patientId': appointment.patient_id,
        'patientName': appointment.patient_name,
        'doctorId': appointment.doctor_id,
        'doctorName': appointment.doctor_name,
        'date': appointment.date.isoformat(),
        'time': appointment.time.strftime('%H:%M:%S'),
        'status': appointment.status
    } for appointment in appointments]

    return jsonify(appointments_list), 200
