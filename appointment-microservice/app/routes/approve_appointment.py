from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required

from app.models.appointment import Appointment
from app.api.auth import get_user_role
from app import db

approve_appointment_bp = Blueprint('approve_appointment', __name__)


# Set appointment status to approved using appointment id
@approve_appointment_bp.route('/appointment/approve/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def approve_appointment(appointment_id):
    user_role = get_user_role()

    if user_role != 'doctor':
        abort(403, description='You do not have permission to approve appointments.')

    appointment = db.session.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        abort(404, description='Appointment not found.')

    appointment.status = 'odobren'
    appointment.save()

    return jsonify(msg='Appointment approved successfully.'), 200
