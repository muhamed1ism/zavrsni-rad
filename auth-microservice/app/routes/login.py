from flask import jsonify, request, abort, Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)

from app import db
from app.models.user import User

login_bp = Blueprint('login', __name__)


# Login user
@login_bp.route('/login', methods=['POST'])
def login():
    if not request.json:
        abort(400, description='No JSON data received in the request.')

    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = db.session.query(User).filter_by(email=email).first()
    if not user or not user.check_password(password):
        abort(401, description='Invalid credentials.')
    
    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify(accessToken=access_token, refreshToken=refresh_token), 200
