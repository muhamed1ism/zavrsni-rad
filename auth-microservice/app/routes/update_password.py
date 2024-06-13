from secrets import compare_digest
from flask import jsonify, request, abort, Blueprint
from flask_jwt_extended import (
    current_user,
    jwt_required
)


update_password_bp = Blueprint('update_password', __name__)


# Update password
@update_password_bp.route('/update-password', methods=['PUT'])
@jwt_required()
def update_password():
    if not request.json:
        abort(400, description='No JSON data received in the request.')


    current_password = request.json.get('currentPassword', '').strip()
    new_password = request.json.get('newPassword', '').strip()

    if not current_password:
        abort(400, description='Current password is required.')
    if not new_password:
        abort(400, description='New password is required.')
    if not current_user.check_password(current_password):
        abort(400, description='Current password is incorrect.')
    if compare_digest(current_password, new_password):
        abort(400, description="New password can't be the same as the current password.")

    current_user.set_password(new_password)
    current_user.save()

    return jsonify(msg='Password updated successfully!'), 200
