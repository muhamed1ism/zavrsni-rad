from flask import Flask, request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,
                                get_jwt_identity, get_jwt, create_refresh_token)
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from secrets import compare_digest
from datetime import datetime, timezone

from models import db, User, TokenBlocklist

# Flask
app = Flask(__name__)
# CORS
CORS(app)
# Config
app.config.from_object('config')
# Database
db.init_app(app)
# Bcrypt
bcrypt = Bcrypt(app)
# JWT
jwt = JWTManager(app)


# noinspection PyUnusedLocal
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


# -------------------------------------------------------------------------------------- #


# Home route
@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the authentication microservice!'


# Register user route
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        email = data['email']
        password = data['password']
        password_confirm = data['password_confirm']

        if not compare_digest(password, password_confirm):
            return jsonify(error='Passwords do not match.'), 400

        existing_email = db.session.query(User).filter_by(email=email).first()
        if existing_email:
            return jsonify(error='Email already taken. Please choose another.'), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            email=email,
            password_hash=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify(msg='User created successfully!'), 200

    except KeyError as e:
        return jsonify(error=f'{str(e)} is required.'), 400

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

    finally:
        db.session.close()


# Login user route
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email = data['email']
        password = data['password']

        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password_hash, password):
            user_access_token = create_access_token(identity=existing_user.id)
            user_refresh_token = create_refresh_token(identity=existing_user.id)

            return jsonify(access_token=user_access_token, refresh_token=user_refresh_token), 200
        else:
            return jsonify(error='Invalid credentials.'), 401

    except KeyError as e:
        return jsonify(error=f'{str(e)} is required.'), 400

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500


# Logout route
@app.route('/logout', methods=['DELETE'])
@jwt_required(verify_type=False)
def modify_token():
    try:
        token = get_jwt()
        jti = token['jti']
        ttype = token['type']
        current_user_id = get_jwt_identity()
        created_at = datetime.now()

        db.session.add(
            TokenBlocklist(
                jti=jti,
                type=ttype,
                user_id=current_user_id,
                created_at=created_at
            )
        )
        db.session.commit()

        return jsonify(msg=f'{ttype.capitalize()} token successfully revoked'), 200

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

    finally:
        db.session.close()


# Refresh token route
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500


# Revoke access token route
@app.route('/revoke-refresh', methods=['POST'])
@jwt_required()
def revoke_refresh_token():
    try:
        jti = get_jwt()['jti']
        current_user_id = get_jwt_identity()
        now = datetime.now(timezone.utc)

        db.session.add(TokenBlocklist(jti=jti, type='refresh', user_id=current_user_id, created_at=now))
        db.session.commit()

        return jsonify(msg='Refresh token successfully revoked'), 200

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

    finally:
        db.session.close()


# Token status route
@app.route('/token-status', methods=['GET'])
@jwt_required()
def token_status():
    try:
        access_token_expires = get_jwt()['exp']
        refresh_token_status = "Valid" if not check_if_token_is_revoked(None, get_jwt()) else "Revoked"

        return jsonify(access_token_expires=access_token_expires, refresh_token_status=refresh_token_status), 200

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500


# Exchange refresh token route
@app.route('/exchange-refresh', methods=['POST'])
@jwt_required(refresh=True)
def exchange_refresh_token():
    try:
        current_user_id = get_jwt_identity()
        user_access_token = create_access_token(identity=current_user_id)
        user_refresh_token = create_refresh_token(identity=current_user_id)

        return jsonify(access_token=user_access_token, refresh_token=user_refresh_token), 200

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500


# Update email route
@app.route('/user/update-email', methods=['PUT'])
@jwt_required()
def update_email():
    try:
        current_user_id = get_jwt_identity()
        current_user = db.session.query(User).get(current_user_id)

        if not current_user:
            return jsonify(error='User not found.'), 404

        data = request.get_json()

        if data['email'] == current_user.email:
            return jsonify(error='Email is the same as the current email.'), 400

        email = data['email']
        existing_email = db.session.query(User).filter(User.email == email, User.id != current_user_id).first()
        if existing_email:
            return jsonify(error='Email already taken. Please choose another.'), 409
        current_user.email = email

        db.session.commit()

        return jsonify(msg='Email updated successfully!'), 200

    except KeyError as e:
        return jsonify(error=f'{str(e)} is required.'), 400

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

    finally:
        db.session.close()


# Update password route
@app.route('/user/update-password', methods=['PUT'])
@jwt_required()
def update_password():
    try:
        current_user_id = get_jwt_identity()
        current_user = db.session.query(User).get(current_user_id)

        if not current_user:
            return jsonify(error='User not found.'), 404

        data = request.get_json()

        current_password = data['current_password']
        new_password = data['new_password']
        new_password_confirm = data['new_password_confirm']

        if not compare_digest(new_password, new_password_confirm):
            return jsonify(error='Passwords do not match.'), 400
        if not bcrypt.check_password_hash(current_user.password_hash, current_password):
            return jsonify(error='Current password is incorrect.'), 400
        if compare_digest(current_password, new_password):
            return jsonify(error='New password cannot be the same as the current password.'), 400

        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        current_user.password_hash = hashed_password
        current_user.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return jsonify(msg='Password updated successfully!'), 200

    except KeyError as e:
        return jsonify(error=f'{str(e)} is required.'), 400

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

    finally:
        db.session.close()


# Delete user route
@app.route('/user/delete', methods=['DELETE'])
@jwt_required()
def delete():
    try:
        current_user_id = get_jwt_identity()
        current_user = db.session.query(User).filter_by(id=current_user_id).first()

        if not current_user:
            return jsonify(error='User not found.'), 404

        db.session.delete(current_user)
        db.session.commit()

        return jsonify(msg='User deleted successfully!'), 200

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

    finally:
        db.session.close()


# Get user route
@app.route('/user', methods=['GET'])
@jwt_required()
def user():
    try:
        current_user_id = get_jwt_identity()
        current_user = db.session.query(User).filter_by(id=current_user_id).first()

        if not current_user:
            return jsonify(error='User not found.'), 404

        return jsonify({
            'id': current_user.id,
            'email': current_user.email,
            'created_at': current_user.created_at,
            'updated_at': current_user.updated_at,
            'role': current_user.role
        }), 200

    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

    finally:
        db.session.close()
