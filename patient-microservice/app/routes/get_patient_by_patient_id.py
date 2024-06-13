from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, current_user

from app import db
from app.api.auth import get_user_role
from app.models.patient import Patient

get_patient_by_patient_id_bp = Blueprint('get_patient_by_patient_id', __name__)


# Get patient information by patient ID
@get_patient_by_patient_id_bp.route('/get-patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_by_id(patient_id):
    user_role = get_user_role()
    if user_role != 'doctor':
        abort(403, description='You do not have permission to view this patient.')
    patient = db.session.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        abort(404, description='Patient not found.')

    return jsonify(patient.to_dict()), 200
