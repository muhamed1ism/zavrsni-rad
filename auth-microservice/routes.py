from flask import Flask, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User
from secrets import compare_digest
from datetime import datetime

app = Flask(__name__)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'tajni_kljuc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id) if user_id else None


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'message': 'You are not logged in.', 'status': 'danger'})


@login_manager.needs_refresh_handler
def refresh():
    return jsonify({'message': 'You need to reauthenticate.', 'status': 'danger'})


@app.get('/')
def home():
    return 'Welcome to the authentication microservice!'


@app.post('/register')
def register():
    data = request.get_json()

    required_fields = ['email', 'password', 'first_name', 'last_name']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields.', 'status': 'danger'})

    email = data['email']
    password = data['password']
    password_confirm = data['password_confirm']
    first_name = data['first_name']
    last_name = data['last_name']
    date_of_birth = data['date_of_birth']
    address = data['address']
    phone_number = data['phone_number']

    if compare_digest(password, password_confirm):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    else:
        return jsonify({'message': 'Passwords do not match.', 'status': 'danger'})

    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        return jsonify({'message': 'Email already taken. Please choose another.', 'status': 'danger'})
    else:
        new_user = User(
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            address=address,
            phone_number=phone_number
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully!', 'status': 'success'})


@app.post('/login')
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        user.last_login = datetime.now()
        db.session.commit()

        response_data = {
            'message': 'Login successful!',
            'status': 'success',
            'user': {
                'id': user.id,
                'email': user.email
            }
        }

        session['user_id'] = user.id

        return jsonify(response_data)
    else:
        return jsonify({'message': 'Invalid email or password.', 'status': 'danger'})


@app.post('/update')
@login_required
def update():
    data = request.get_json()

    user = db.session.query(User).filter_by(id=current_user.id).first()

    match data:
        case {'email': _}:
            user.email = data['email']
        case {'password': _}:
            user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        case {'first_name': _}:
            user.first_name = data['first_name']
        case {'last_name': _}:
            user.last_name = data['last_name']
        case {'date_of_birth': _}:
            user.date_of_birth = data['date_of_birth']
        case {'address': _}:
            user.address = data['address']
        case {'phone_number': _}:
            user.phone_number = data['phone_number']
        case _:
            return jsonify({'message': 'Invalid request.', 'status': 'danger'})

    db.session.commit()

    return jsonify({'message': 'User updated successfully!', 'status': 'success'})


@app.post('/delete')
@login_required
def delete():
    user = db.session.query(User).filter_by(id=current_user.id).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully!', 'status': 'success'})


@app.post('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful!', 'status': 'success'})


@app.get('/check_session')
@login_required
def check_session():
    return jsonify({'message': 'Session active!', 'user_id': current_user.id, 'status': 'success'})


@app.get('/user')
@login_required
def get_user():
    user_data = {
        'id': current_user.id,
        'email': current_user.email,
        'name': current_user.first_name + ' ' + current_user.last_name
    }
    return jsonify(user_data)


@app.get('/user/<string:string>')
@login_required
def get_user_string(string):
    match string:
        case 'email':
            email = current_user.email
            return jsonify({'email': email})
        case 'first_name':
            first_name = current_user.first_name
            return jsonify({'first_name': first_name})
        case 'last_name':
            last_name = current_user.last_name
            return jsonify({'last_name': last_name})
        case 'address':
            address = current_user.address
            return jsonify({'address': address})
        case 'phone_number':
            phone_number = current_user.phone_number
            return jsonify({'phone_number': phone_number})
        case 'date_of_birth':
            date_of_birth = current_user.date_of_birth
            return jsonify({'date_of_birth': date_of_birth})
        case _:
            return jsonify({'message': 'Invalid request.', 'status': 'danger'})


@app.get('/user/last_login')
@login_required
def get_user_last_login():
    last_login = current_user.last_login
    return jsonify({'last_login': last_login})
