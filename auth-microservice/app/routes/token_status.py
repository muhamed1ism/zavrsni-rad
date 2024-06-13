from flask import jsonify, Blueprint
from flask_jwt_extended import (
    get_jwt,
    jwt_required
)

from app import jwt, db
from app.models.token_blocklist import TokenBlocklist

token_status_bp = Blueprint('token_status', __name__)


# Check if token is revoked
# noinspection PyUnusedLocal
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload['jti']
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


# Token status
@token_status_bp.route('/token-status', methods=['GET'])
@jwt_required()
def token_status():
    access_token_expires = get_jwt()['exp']
    refresh_token_status = "Valid" if not check_if_token_is_revoked(None, get_jwt()) else "Revoked"
    return jsonify(accessTokenExpires=access_token_expires, refreshTokenStatus=refresh_token_status), 200
