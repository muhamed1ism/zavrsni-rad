from datetime import datetime
from secrets import compare_digest
from flask import jsonify, request, abort
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required, JWTManager
)

from models import User, TokenBlocklist, db

# CORS
CORS_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5001',
    'http://localhost:5002',
    'http://localhost:5003'
]
cors = CORS(origins=CORS_ORIGINS)
# JWT
jwt = JWTManager()
# Bcrypt
bcrypt = Bcrypt()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


# Check if token is revoked
# noinspection PyUnusedLocal
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


def app_routes(app):
    app_route_home(app)
    app_route_register(app)
    app_route_login(app)
    app_route_logout(app)
    app_route_refresh_token(app)
    app_route_revoke_refresh_token(app)
    app_route_token_status(app)
    app_route_exchange_refresh_token(app)
    app_route_get_user(app)
    app_route_update_email(app)
    app_route_update_password(app)
    app_route_delete_user(app)


# -------------------------------------------------------------------------------------------------------------------- #


# Home route
def app_route_home(app):
    @app.route('/', methods=['GET'])
    def home():
        return jsonify(msg='Auth service is up and running.'), 200


# Register user route
def app_route_register(app):

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()

        if data is None:
            return jsonify(error='No data provided.'), 400

        if data['email'] == '' or 'email' not in data or data['email'].isspace():
            return jsonify(error='Email is required.'), 400

        if data['password'] == '' or 'password' not in data or data['password'].isspace():
            return jsonify(error='Password is required.'), 400

        if data['passwordConfirm'] == '' or 'passwordConfirm' not in data or data['passwordConfirm'].isspace():
            return jsonify(error='Password confirmation is required.'), 400

        email = data['email']
        password = data['password']
        password_confirm = data['passwordConfirm']
        role = data['role']

        if not compare_digest(password, password_confirm):
            return jsonify(error='Passwords do not match.'), 400

        existing_email = db.session.query(User).filter_by(email=email).first()

        if existing_email:
            return jsonify(error='Email already taken. Please choose another.'), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            email=email,
            password_hash=hashed_password,
            role=role
        )

        access_token = create_access_token(identity=new_user.id, fresh=True)
        refresh_token = create_refresh_token(identity=new_user.id)

        try:
            db.session.add(new_user)
            db.session.commit()

        except Exception as e:
            return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

        finally:
            db.session.close()


        return (
            jsonify(msg='User created successfully!')
            and jsonify(accessToken=access_token, refreshToken=refresh_token), 201
        )


# Login user route
def app_route_login(app):

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()

        if data is None:
            return jsonify(error='No data provided.'), 400

        if data['email'] == '' or 'email' not in data or data['email'].isspace():
            return jsonify(error='Email is required.'), 400

        if data['password'] == '' or 'password' not in data or data['password'].isspace():
            return jsonify(error='Password is required.'), 400

        email = data['email']
        password = data['password']

        existing_user = db.session.query(User).filter_by(email=email).first()

        if existing_user and bcrypt.check_password_hash(existing_user.password_hash, password):
            access_token = create_access_token(identity=existing_user.id, fresh=True)
            refresh_token = create_refresh_token(identity=existing_user.id)

            return jsonify(accessToken=access_token, refreshToken=refresh_token), 200
        else:
            return jsonify(error='Invalid credentials.'), 401


# Logout route
def app_route_logout(app):

    @app.route('/logout', methods=['DELETE'])

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


# Refresh token route
def app_route_refresh_token(app):

    @app.route('/refresh-token', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh_token():
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)
        return jsonify(accessToken=access_token), 200


# Revoke access token route
def app_route_revoke_refresh_token(app):

    @app.route('/revoke-refresh-token', methods=['POST'])
    @jwt_required()
    def revoke_refresh_token():
        jti = get_jwt()['jti']
        user_id = get_jwt_identity()
        now = datetime.now()

        try:
            db.session.add(TokenBlocklist(jti=jti, type='refresh', user_id=user_id, created_at=now))
            db.session.commit()

        except Exception as e:
            return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

        finally:
            db.session.close()

        return jsonify(msg='Refresh token successfully revoked'), 200


# Token status route
def app_route_token_status(app):

    @app.route('/token-status', methods=['GET'])
    @jwt_required()
    def token_status():
        access_token_expires = get_jwt()['exp']
        refresh_token_status = "Valid" if not check_if_token_is_revoked(None, get_jwt()) else "Revoked"

        return jsonify(accessTokenExpires=access_token_expires, refreshTokenStatus=refresh_token_status), 200


# Exchange refresh token route
def app_route_exchange_refresh_token(app):

    @app.route('/exchange-refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def exchange_refresh_token():
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        return jsonify(accessToken=access_token, refreshToken=refresh_token), 200


# Get user route
def app_route_get_user(app):

    @app.route('/get-user', methods=['GET'])
    @jwt_required()
    def get_user():
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify(error='User not found.'), 404

        return jsonify({
            'id': user.id,
            'email': user.email,
            'createdAt': user.created_at,
            'updatedAt': user.updated_at,
            'role': user.role
        }), 200


# Update email route
def app_route_update_email(app):

    @app.route('/update-email', methods=['PUT'])
    @jwt_required()
    def update_email():
        data = request.get_json()
        user_id = get_jwt_identity()
        user = db.session.query(User).get(user_id)

        if not user:
            return jsonify(error='User not found.'), 404

        if data is None:
            return jsonify(error='No data provided.'), 400

        if not data['email'] or 'email' not in data or data['email'].isspace():
            return jsonify(error='Email is required.'), 400

        if data['email'] == user.email:
            return jsonify(error='Email is the same as the current email.'), 400

        existing_email = db.session.query(User).filter_by(email=data['email']).first()

        if existing_email:
            return jsonify(error='Email already taken. Please choose another.'), 409

        user.email = data['email']

        try:
            db.session.commit()

        except Exception as e:
            return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

        finally:
            db.session.close()

        return jsonify(msg='Email updated successfully!'), 200


# Update password route
def app_route_update_password(app):

    @app.route('/update-password', methods=['PUT'])
    @jwt_required()
    def update_password():
        data = request.get_json()
        user_id = get_jwt_identity()
        user = db.session.query(User).get(user_id)

        if not user:
            return jsonify(error='User not found.'), 404

        if data is None:
            return jsonify(error='No data provided.'), 400

        if not data['currentPassword'] or 'currentPassword' not in data or data['currentPassword'].isspace():
            return jsonify(error='Current password is required.'), 400

        if not data['newPassword'] or 'newPassword' not in data or data['newPassword'].isspace():
            return jsonify(error='New password is required.'), 400

        if (data['newPasswordConfirm'] == '' or 'newPasswordConfirm' not in data
                or data['newPasswordConfirm'].isspace()):
            return jsonify(error='New password confirmation is required.'), 400

        current_password = data['currentPassword']
        new_password = data['newPassword']
        new_password_confirm = data['newPasswordConfirm']

        if not compare_digest(new_password, new_password_confirm):
            return jsonify(error='Passwords do not match.'), 400

        if not bcrypt.check_password_hash(user.password_hash, current_password):
            return jsonify(error='Current password is incorrect.'), 400

        if compare_digest(current_password, new_password):
            return jsonify(error='New password cannot be the same as the current password.'), 400

        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        user.password_hash = hashed_password

        try:
            db.session.commit()

        except Exception as e:
            return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

        finally:
            db.session.close()

        return jsonify(msg='Password updated successfully!'), 200


# Delete user route
def app_route_delete_user(app):

    @app.route('/delete-user', methods=['DELETE'])
    @jwt_required()
    def delete_user():
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify(error='User not found.'), 404

        try:
            db.session.delete(user)
            db.session.commit()

        except Exception as e:
            return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

        finally:
            db.session.close()

        return jsonify(msg='User deleted successfully!'), 200

