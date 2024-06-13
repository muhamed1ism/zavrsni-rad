from flask import jsonify, abort, Blueprint

from app import db
from app.models.doctor import Doctor

get_doctor_by_doctor_id_bp = Blueprint('get_doctor_by_doctor_id', __name__)


# Get doctor information by doctor ID
@get_doctor_by_doctor_id_bp.route('/get-doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    doctor = db.session.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        abort(404, description='Doctor not found.')

    return jsonify(doctor.to_dict()), 200
