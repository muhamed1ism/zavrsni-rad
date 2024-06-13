from datetime import datetime
from flask import jsonify, abort, Blueprint
from flask_jwt_extended import (
    get_jwt,
    jwt_required
)

from app.models.token_blocklist import TokenBlocklist

logout_bp = Blueprint('logout', __name__)


# Logout user
@logout_bp.route('/logout', methods=['DELETE'])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token['jti']
    ttype = token['type']
    now = datetime.now()

    if ttype not in ('access', 'refresh'):
        abort(400, description=f"Invalid token type: {ttype}")

    token_blacklist = TokenBlocklist(jti=jti, type=ttype, created_at=now)
    token_blacklist.save()

    return jsonify(msg=f'{ttype.capitalize()} token successfully revoked'), 200
