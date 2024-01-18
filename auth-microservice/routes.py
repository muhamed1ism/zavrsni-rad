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
    return User.query.get(int(user_id)) if user_id else None


@app.route('/')
def home():
    return 'Welcome to the authentication microservice!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()

        # Check if all required fields are present
        required_fields = ['email', 'password', 'first_name', 'last_name']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields.', 'status': 'danger'})

        email = data['email']
        password = data['password']
        password_confirmation = data['password_confirmation']
        first_name = data['first_name']
        last_name = data['last_name']
        date_of_birth = data['date_of_birth']
        address = data['address']
        phone_number = data['phone_number']

        if compare_digest(password, password_confirmation):
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        else:
            return jsonify({'message': 'Passwords do not match.', 'status': 'danger'})

        existing_email = User.query.filter_by(email=email).first()
        # Check if user already exists
        if existing_email:
            return jsonify({'message': 'Email already taken. Please choose another.', 'status': 'danger'})
        else:
            # Create a new user
            new_user = User(email=email, password_hash=hashed_password, first_name=first_name,
                            last_name=last_name, date_of_birth=date_of_birth, address=address, phone_number=phone_number
                            )
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User created successfully!', 'status': 'success'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
    else:
        return jsonify({'message': 'Login page!', 'status': 'success'})


@app.route('/update', methods=['POST'])
@login_required
def update():
    data = request.get_json()

    user = User.query.filter_by(id=current_user.id).first()

    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'date_of_birth' in data:
        user.date_of_birth = data['date_of_birth']
    if 'address' in data:
        user.address = data['address']
    if 'phone_number' in data:
        user.phone_number = data['phone_number']

    db.session.commit()

    return jsonify({'message': 'User updated successfully!', 'status': 'success'})


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    user = User.query.filter_by(id=current_user.id).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully!', 'status': 'success'})


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful!', 'status': 'success'})


@app.route('/check_session', methods=['GET'])
@login_required
def check_session():
    return jsonify({'message': 'Session active!', 'user_id': current_user.id, 'status': 'success'})


@app.route('/user', methods=['GET'])
@login_required
def get_user():
    user_data = {
        'id': current_user.id,
        'email': current_user.email,
        'name': current_user.first_name + ' ' + current_user.last_name
    }
    return jsonify(user_data)


@app.route('/user/address', methods=['GET'])
@login_required
def get_user_address():
    address = current_user.address
    return jsonify({'address': address})


@app.route('/user/phone_number', methods=['GET'])
@login_required
def get_user_phone_number():
    phone_number = current_user.phone_number
    return jsonify({'phone_number': phone_number})


@app.route('/user/last_login', methods=['GET'])
@login_required
def get_user_last_login():
    last_login = current_user.last_login
    return jsonify({'last_login': last_login})


@app.route('/user/date_of_birth', methods=['GET'])
@login_required
def get_user_date_of_birth():
    date_of_birth = current_user.date_of_birth
    return jsonify({'date_of_birth': date_of_birth})


if __name__ == '__main__':

    app.run(debug=True)
