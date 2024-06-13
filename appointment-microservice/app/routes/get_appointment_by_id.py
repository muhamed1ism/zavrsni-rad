from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required

from app.models.appointment import Appointment
from app.api.doctor import get_doctor
from app.api.patient import get_patient_id
from app.api.auth import get_user_role
from app import db

get_appointment_by_id_bp = Blueprint('get_appointment_by_id', __name__)


# Get appointment by appointment ID
@get_appointment_by_id_bp.route('/get-appointment/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment_by_id(appointment_id):
    appointment = db.session.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        abort(404, description='Appointment not found.')

    user_role = get_user_role()

    if user_role == 'patient' and appointment.patient_id != get_patient_id():
        abort(403, description='You do not have permission to view this appointment.')
    elif user_role == 'doctor' and appointment.doctor_id != get_doctor():
        abort(403, description='You do not have permission to view this appointment.')

    time = appointment.time.strftime('%H:%M:%S')

    return jsonify({
        'id': appointment.id,
        'patientId': appointment.patient_id,
        'patientName': appointment.patient_name,
        'doctorId': appointment.doctor_id,
        'doctorName': appointment.doctor_name,
        'date': appointment.date,
        'time': time,
        'status': appointment.status
    }), 200
