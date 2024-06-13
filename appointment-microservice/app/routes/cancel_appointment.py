from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required

from app.models.appointment import Appointment
from app.api.auth import get_user_role
from app import db

cancel_appointment_bp = Blueprint('cancel_appointment', __name__)


# Set appointment status to canceled using appointment id
@cancel_appointment_bp.route('/appointment/cancel/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def cancel_appointment(appointment_id):
    user_role = get_user_role()

    if user_role != 'patient':
        abort(403, description='You do not have permission to cancel appointments.')

    appointment = db.session.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        abort(404, description='Appointment not found.')

    appointment.status = 'otkazan'
    appointment.save()

    return jsonify(msg='Appointment canceled successfully.'), 200
