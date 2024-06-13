from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required

from app.models.appointment import Appointment
from app.api.auth import get_user_role
from app import db

restore_appointment_bp = Blueprint('restore_appointment', __name__)


# Set appointment back to pending status using appointment id
@restore_appointment_bp.route('/appointment/restore/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def restore_appointment(appointment_id):
    user_role = get_user_role()

    if user_role != 'patient':
        abort(403, description='You do not have permission to restore appointments.')

    appointment = db.session.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        abort(404, description='Appointment not found.')

    appointment.status = 'na čekanju'
    appointment.save()

    return jsonify(msg='Appointment restored successfully.'), 200
