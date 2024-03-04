from datetime import datetime
from secrets import compare_digest
from flask import jsonify, request, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required
)

from app.extensions import db, jwt, argon2, bp
from app.models import User, TokenBlocklist


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).first()


# Check if token is revoked
# noinspection PyUnusedLocal
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload['jti']
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


# -------------------------------------------------------------------------------------------------------------------- #


# Home
@bp.route('/', methods=['GET'])
def home():
    return jsonify(msg='Auth service is up and running.'), 200


# Register user
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if data is None:
        abort(400, description='No data provided.')

    if data['email'] == '' or 'email' not in data or data['email'].isspace():
        abort(400, description='Email is required.')

    if data['password'] == '' or 'password' not in data or data['password'].isspace():
        abort(400, description='Password is required.')

    if data['passwordConfirm'] == '' or 'passwordConfirm' not in data or data['passwordConfirm'].isspace():
        abort(400, description='Password confirmation is required.')

    email = data['email']
    password = data['password']
    password_confirm = data['passwordConfirm']
    role = data['role']

    if not compare_digest(password, password_confirm):
        abort(400, description='Passwords do not match.')

    existing_email = db.session.query(User).filter_by(email=email).first()

    if existing_email:
        abort(409, description='Email already taken. Please choose another.')

    hashed_password = argon2.generate_password_hash(password)

    new_user = User(
        email=email,
        password_hash=hashed_password,
        role=role
    )

    try:
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        abort(500, description=f'An unexpected error occurred: {str(e)}')

    finally:
        db.session.close()

    return jsonify(msg='User created successfully!'), 201


# Login user
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if data is None:
        abort(400, description='No data provided.')

    if data['email'] == '' or 'email' not in data or data['email'].isspace():
        abort(400, description='Email is required.')

    if data['password'] == '' or 'password' not in data or data['password'].isspace():
        abort(400, description='Password is required.')

    email = data['email']
    password = data['password']

    existing_user = db.session.query(User).filter_by(email=email).first()

    if existing_user and argon2.check_password_hash(existing_user.password_hash, password):
        access_token = create_access_token(identity=existing_user.id, fresh=True)
        refresh_token = create_refresh_token(identity=existing_user.id)

        return jsonify(accessToken=access_token, refreshToken=refresh_token), 200
    else:
        abort(401, description='Invalid credentials.')


# Logout user
@bp.route('/logout', methods=['DELETE'])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token['jti']
    ttype = token['type']
    now = datetime.now()

    try:
        if ttype not in ('access', 'refresh'):
            abort(400, description=f"Invalid token type: {ttype}")

        db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        abort(500, description=f"An unexpected error occurred: {str(e)}")

    finally:
        db.session.close()

    return jsonify(msg=f'{ttype.capitalize()} token successfully revoked'), 200


# Refresh token
@bp.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id, fresh=False)
    return jsonify(accessToken=access_token), 200


# Token status
@bp.route('/token-status', methods=['GET'])
@jwt_required()
def token_status():
    access_token_expires = get_jwt()['exp']
    refresh_token_status = "Valid" if not check_if_token_is_revoked(None, get_jwt()) else "Revoked"

    return jsonify(accessTokenExpires=access_token_expires, refreshTokenStatus=refresh_token_status), 200


# Exchange refresh token
@bp.route('/exchange-refresh', methods=['POST'])
@jwt_required(refresh=True)
def exchange_refresh_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    return jsonify(accessToken=access_token, refreshToken=refresh_token), 200


# Get user route
@bp.route('/get-user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = db.session.query(User).filter_by(id=user_id).first()

    if not user:
        abort(404, description='User not found.')

    return jsonify({
        'id': user.id,
        'email': user.email,
        'createdAt': user.created_at,
        'updatedAt': user.updated_at,
        'role': user.role
    }), 200


# Update email
@bp.route('/update-email', methods=['PUT'])
@jwt_required()
def update_email():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        abort(404, description='User not found.')

    if data is None:
        abort(400, description='No data provided.')

    if not data['email'] or 'email' not in data or data['email'].isspace():
        abort(400, description='Email is required.')

    if data['email'] == user.email:
        abort(400, description='Email is the same as the current email.')

    existing_email = db.session.query(User).filter_by(email=data['email']).first()

    if existing_email:
        abort(409, description='Email already taken. Please choose another.')

    user.email = data['email']

    try:
        db.session.commit()

    except Exception as e:
        abort(500, description=f'An unexpected error occurred: {str(e)}')

    finally:
        db.session.close()

    return jsonify(msg='Email updated successfully!'), 200


# Update password
@bp.route('/update-password', methods=['PUT'])
@jwt_required()
def update_password():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        abort(404, description='User not found.')

    if data is None:
        abort(400, description='No data provided.')

    if not data['currentPassword'] or 'currentPassword' not in data or data['currentPassword'].isspace():
        abort(400, description='Current password is required.')

    if not data['newPassword'] or 'newPassword' not in data or data['newPassword'].isspace():
        abort(400, description='New password is required.')

    if (data['newPasswordConfirm'] == '' or 'newPasswordConfirm' not in data
            or data['newPasswordConfirm'].isspace()):
        abort(400, description='New password confirmation is required.')

    current_password = data['currentPassword']
    new_password = data['newPassword']
    new_password_confirm = data['newPasswordConfirm']

    if not compare_digest(new_password, new_password_confirm):
        abort(400, description='Passwords do not match.')

    if not argon2.check_password_hash(user.password_hash, current_password):
        abort(400, description='Current password is incorrect.')

    if compare_digest(current_password, new_password):
        abort(400, description='New password cannot be the same as the current password.')

    hashed_password = argon2.generate_password_hash(new_password)

    user.password_hash = hashed_password

    try:
        db.session.commit()

    except Exception as e:
        abort(500, description=f'An unexpected error occurred: {str(e)}')

    finally:
        db.session.close()

    return jsonify(msg='Password updated successfully!'), 200


# Delete user
@bp.route('/delete-user', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = db.session.query(User).filter_by(id=user_id).first()

    if not user:
        abort(404, description='User not found.')

    try:
        db.session.delete(user)
        db.session.commit()

    except Exception as e:
        abort(500, description=f'An unexpected error occurred: {str(e)}')

    finally:
        db.session.close()

    return jsonify(msg='User deleted successfully!'), 200
