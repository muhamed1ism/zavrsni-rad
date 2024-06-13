from flask import jsonify, Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    jwt_required
)

exchange_refresh_bp = Blueprint('exchange_refresh', __name__)


# Exchange refresh token
@exchange_refresh_bp.route('/exchange-refresh', methods=['POST'])
@jwt_required(refresh=True)
def exchange_refresh_token():
    access_token = create_access_token(identity=current_user.id)
    refresh_token = create_refresh_token(identity=current_user.id)
    return jsonify(accessToken=access_token, refreshToken=refresh_token), 200
