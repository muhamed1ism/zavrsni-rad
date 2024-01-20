from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from secrets import compare_digest
from datetime import datetime, timedelta, timezone
from models import db, User, TokenBlocklist

app = Flask(__name__)
CORS(app)


if app.config['TESTING']:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

ACCESS_EXPIRES = timedelta(hours=1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'tajni_kljuc'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the authentication microservice!'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    password_confirm = data['password_confirm']

    fields = ['email', 'password', 'password_confirm']
    for field in fields:
        if field not in data:
            return jsonify(msg=f'{field} is required.'), 400

    if not compare_digest(password, password_confirm):
        return jsonify({'msg': 'Passwords do not match.'}), 400

    existing_email = db.session.query(User).filter_by(email=email).first()
    if existing_email:
        return jsonify(msg='Email already taken. Please choose another.'), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        email=email,
        password_hash=hashed_password,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(msg='User created successfully!'), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    if not email or not password:
        return jsonify(msg='Email and password are required.'), 400

    user = db.session.query(User).filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(msg='Invalid credentials.'), 401


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token), 200


@app.route('/logout', methods=['DELETE'])
@jwt_required(verify_type=False)
def modify_token():
    token = get_jwt()
    jti = token['jti']
    ttype = token['type']
    user_id = get_jwt_identity()
    now = datetime.now(timezone.utc)

    db.session.add(TokenBlocklist(jti=jti, type=ttype, user_id=user_id, created_at=now))
    db.session.commit()

    return jsonify(msg=f'{ttype.capitalize()} token successfully revoked'), 200


@app.route('/update-email', methods=['POST'])
@jwt_required()
def update_email():
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify(msg='User not found.'), 404

    data = request.get_json()

    if 'email' not in data:
        return jsonify(msg='Email is required.'), 400

    email = data['email']
    existing_email = db.session.query(User).filter(User.email == email, User.id != user_id).first()
    if existing_email:
        return jsonify(msg='Email already taken. Please choose another.'), 409
    user.email = email

    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify(msg='Email updated successfully!'), 200


@app.route('/update-password', methods=['POST'])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify(msg='User not found.'), 404

    data = request.get_json()

    if 'current_password' not in data or 'new_password' not in data or 'new_password_confirm' not in data:
        return jsonify(msg='All fields are required.'), 400

    current_password = data['current_password']
    new_password = data['new_password']
    new_password_confirm = data['new_password_confirm']

    if not compare_digest(new_password, new_password_confirm):
        return jsonify(msg='Passwords do not match.'), 400
    if not bcrypt.check_password_hash(user.password_hash, current_password):
        return jsonify(msg='Current password is incorrect.'), 400
    if compare_digest(current_password, new_password):
        return jsonify(msg='New password cannot be the same as the current password.'), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password_hash = hashed_password
    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify(msg='Password updated successfully!'), 200


@app.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    user_id = get_jwt_identity()
    user = db.session.query(User).filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify(msg='User deleted successfully!'), 200
