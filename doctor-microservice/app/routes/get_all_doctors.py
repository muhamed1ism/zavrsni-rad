from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required

from app import db
from app.models.doctor import Doctor

get_all_doctors_bp = Blueprint('get_all_doctors', __name__)


# Get all doctors
@get_all_doctors_bp.route('/get-doctors', methods=['GET'])
@jwt_required()
def get_all_doctors():
    doctors = db.session.query(Doctor).all()

    if not doctors:
        abort(404, description='No doctors found.')

    doctors_list = []
    for doctor in doctors:
        doctors_list.append({
            'id': doctor.id,
            'name': f'{doctor.first_name} {doctor.last_name}',
            'specialty': doctor.specialty,
        })

    return jsonify(doctors_list), 200
