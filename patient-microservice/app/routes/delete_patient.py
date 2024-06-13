from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from app import db
from app.models.patient import Patient

delete_patient_bp = Blueprint('delete_patient', __name__)


# Delete a patient profile
@delete_patient_bp.route('/delete-patient', methods=['DELETE'])
@jwt_required()
def delete_patient():
    if not current_user:
        abort(404, description='Patient has no profile')

    current_user.delete()

    return jsonify(msg='Patient profile deleted successfully!'), 200
