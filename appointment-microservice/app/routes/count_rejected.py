from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required

from app.models.appointment import Appointment
from app.api.doctor import get_doctor_id
from app.api.auth import get_user_role
from app import db

count_rejected_bp = Blueprint('count_rejected', __name__)


# Get number of rejected appointments
@count_rejected_bp.route('/appointment/count-rejected', methods=['GET'])
@jwt_required()
def count_rejected_appointments():
    user_role = get_user_role()

    if user_role != 'doctor':
        abort(403, description='You do not have permission to count appointments.')

    doctor_id = get_doctor_id()

    appointments = db.session.query(Appointment).filter(Appointment.doctor_id == doctor_id,
                                                        Appointment.status == 'rejected').count()

    return jsonify(appointments), 200
