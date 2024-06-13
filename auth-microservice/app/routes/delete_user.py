from flask import jsonify, Blueprint
from flask_jwt_extended import (
    current_user,
    jwt_required
)


delete_user_bp = Blueprint('delete_user', __name__)


# Delete user
@delete_user_bp.route('/delete-user', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user.delete()
    return jsonify(msg='User deleted successfully!'), 200
