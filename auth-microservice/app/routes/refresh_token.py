from flask import jsonify, Blueprint
from flask_jwt_extended import (
    create_access_token,
    current_user,
    jwt_required
)

refresh_token_bp = Blueprint('refresh_token', __name__)


# Refresh token
@refresh_token_bp.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    access_token = create_access_token(identity=current_user.id, fresh=False)
    return jsonify(accessToken=access_token), 200
