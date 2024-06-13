from flask import jsonify, request, abort, Blueprint
from flask_jwt_extended import (
    current_user,
    jwt_required
)

from app import db
from app.models.user import User

update_email_bp = Blueprint('update_email', __name__)


# Update email
@update_email_bp.route('/update-email', methods=['PUT'])
@jwt_required()
def update_email():
    if not request.json:
        abort(400, description='No JSON data received in the request.')

    email = request.json.get('email', '').strip()

    if not email:
        abort(400, description='Email is required.')
    if email == current_user.email: 
        abort(400, description='Email is the same as the current email.')
    if db.session.query(User).filter_by(email=email).first():
        abort(409, description='Email already registered.')

    current_user.email = email
    current_user.save()

    return jsonify(msg='Email updated successfully!'), 200
