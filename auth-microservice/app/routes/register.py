from flask import jsonify, request, abort, Blueprint

from app import db
from app.models.user import User

register_bp = Blueprint('register', __name__)


# Register user
@register_bp.route('/register', methods=['POST'])
def register():
    if not request.json:
        abort(400, description='No JSON data received in the request.')

    email = request.json.get('email', '').strip()
    password = request.json.get('password', '').strip()
    role = request.json.get('role', 'patient')

    if not email:
        abort(400, description='Email is required.')
    if not password:
        abort(400, description='Password is required.')
    if db.session.query(User).filter_by(email=email).first():
        abort(409, description='Email already registered.')

    new_user = User(email=email, role=role)
    new_user.set_password(password)
    new_user.save()

    return jsonify(msg='User created successfully!'), 201
