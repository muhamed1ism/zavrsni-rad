import datetime
from flask import jsonify, abort, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models.appointment import Appointment
from app.api.patient import get_patient_id, get_patient_name
from app.api.doctor import get_doctor_name

create_appointment_bp = Blueprint('create_appointment', __name__)


# Create appointment
@create_appointment_bp.route('/create-appointment', methods=['POST'])
@jwt_required()
def create_appointment():
    doctor_id = request.json.get('doctorId', None)
    date = request.json.get('date', None)
    time = request.json.get('time', None)

    if not all([doctor_id, date, time]):
        abort(400, description='Doctor ID, Date and Time are required.')

    patient_id = get_patient_id()
    patient_name = get_patient_name()
    doctor_name = get_doctor_name(doctor_id)

    formatted_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    formatted_time = datetime.datetime.strptime(
        f"{time['hours']}:{time['minutes']}:00",
        '%H:%M:%S'
    ).time()

    new_appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        date=formatted_date,
        time=formatted_time,
        patient_name=patient_name,
        doctor_name=doctor_name,
        status='na čekanju'
    )
    new_appointment.save()

    return jsonify(msg='Appointment created successfully.'), 201
