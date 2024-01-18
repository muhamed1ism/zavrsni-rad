import pytest
from routes import app
from models import db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

        db.drop_all()


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Welcome to the authentication microservice!'


def test_register(client):
    data = {
        'email': 'test@example.com',
        'password': 'password',
        'password_confirm': 'password',
        'first_name': 'Test',
        'last_name': 'User',
        'date_of_birth': '01/01/2000',
        'address': '123 Test St',
        'phone_number': '0612345678'
    }

    response = client.post('/register', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_login(client):
    test_register(client)

    data = {
        'email': 'test@example.com',
        'password': 'password'
    }

    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_update(client):
    test_login(client)

    data = {
        'first_name': 'Updated'
    }

    response = client.post('/update', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_logout(client):
    test_login(client)

    response = client.post('/logout')
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_check_session(client):
    test_login(client)

    response = client.get('/check-session')
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_get_user(client):
    test_login(client)

    response = client.get('/user')
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_get_user_string(client):
    test_login(client)

    strings = ['email', 'first_name', 'last_name', 'address', 'phone_number', 'date_of_birth']

    for string in strings:
        response = client.get(f'/user/{string}')
        assert response.status_code == 200
        assert response.json['status'] == 'success'


def test_get_user_last_login(client):
    test_login(client)

    response = client.get('/user/last-login')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
