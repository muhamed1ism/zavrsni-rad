from flask import jsonify, Blueprint, abort
from flask_jwt_extended import jwt_required, current_user


get_patient_bp = Blueprint('get_patient', __name__)


# Get the current patient's profile
@get_patient_bp.route('/get-patient', methods=['GET'])
@jwt_required()
def get_patient():
    if not current_user:
        abort(404, description='Patient has no profile')
    return jsonify(current_user.to_dict()), 200
