from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, current_user

get_doctor_bp = Blueprint('get_doctor', __name__)


# Get the current doctor's profile
@get_doctor_bp.route('/get-doctor', methods=['GET'])
@jwt_required()
def get_doctor():
    if not current_user:
        abort(404, description='Doctor has no profile')
    return jsonify(current_user.to_dict()), 200
