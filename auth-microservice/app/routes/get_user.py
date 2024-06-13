from flask import jsonify, Blueprint
from flask_jwt_extended import (
    current_user,
    jwt_required
)

get_user_bp = Blueprint('get_user', __name__)


# Get user route
@get_user_bp.route('/get-user', methods=['GET'])
@jwt_required()
def get_user():
    return jsonify(current_user.to_dict()), 200
