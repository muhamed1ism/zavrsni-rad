from flask import Flask, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from secrets import compare_digest
from datetime import datetime
from models import db, User

app = Flask(__name__)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tajni_kljuc'

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
    return jsonify({'message': 'You need to re-authenticate.', 'status': 'danger'})


@app.get('/')
def home():
    return 'Welcome to the authentication microservice!'


@app.post('/register')
def register():
    data = request.get_json()

    if 'email' not in data:
        return jsonify({'message': 'Email required.', 'status': 'danger'})
    if 'password' not in data:
        return jsonify({'message': 'Password required.', 'status': 'danger'})
    if 'password_confirm' not in data:
        return jsonify({'message': 'Password confirmation required.', 'status': 'danger'})

    email = data['email']
    password = data['password']
    password_confirm = data['password_confirm']

    if compare_digest(password, password_confirm):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    else:
        return jsonify({'message': 'Passwords do not match.', 'status': 'danger'})

    existing_email = db.session.query(User).filter_by(email=email).first()

    if existing_email:
        return jsonify({'message': 'Email already taken. Please choose another.', 'status': 'danger'})
    else:
        # noinspection PyArgumentList
        new_user = User(
            email=email,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully!', 'status': 'success'})


@app.post('/login')
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    user = db.session.query(User).filter_by(email=email).first()
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

    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user.updated_at = datetime.now()

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


@app.get('/check-session')
@login_required
def check_session():
    return jsonify({'message': 'Session active!', 'user_id': current_user.id, 'status': 'success'})


@app.get('/user')
@login_required
def get_user():
    user_data = {
        'id': current_user.id,
        'email': current_user.email
    }
    return jsonify(user_data) and jsonify({'status': 'success'})


@app.get('/user/id')
@login_required
def get_user_id():
    return jsonify({'id': current_user.id, 'status': 'success'})


@app.get('/user/email')
@login_required
def get_user_email():
    return jsonify({'email': current_user.email, 'status': 'success'})


@app.get('/check-user/<int:user_id>')
def check_user(user_id):
    user_exists = db.session.query(User).filter_by(id=user_id).first() is not None
    return jsonify({'user_exists': user_exists})


@app.get('/user/last-login')
@login_required
def get_user_last_login():
    last_login = current_user.last_login
    return jsonify({'last-login': last_login, 'status': 'success'})
