from flask import jsonify, abort, Blueprint
from flask_jwt_extended import jwt_required, current_user

delete_doctor_bp = Blueprint('delete_doctor', __name__)


# Delete a doctor profile
@delete_doctor_bp.route('/delete-doctor', methods=['DELETE'])
@jwt_required()
def delete_profile():
    if not current_user:
        abort(404, description='Doctor has no profile')

    current_user.delete()

    return jsonify(msg='Doctor profile deleted successfully!'), 200
