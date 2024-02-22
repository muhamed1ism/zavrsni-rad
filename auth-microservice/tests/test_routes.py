import pytest

import tests.test_config as test_config
from app import create_app
from app.models import db

user = {
    'email': 'test@example.com',
    'password': 'password',
    'passwordConfirm': 'password',
    'role': 'patient'
}


def authorization_header(token):
    return {'Authorization': 'Bearer ' + token}


config = test_config.__dict__
app = create_app(test_config=config)


@pytest.fixture
def client():
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_register(client):
    response = client.post('/register', json=user)
    assert response.status_code == 201


def test_login(client):
    test_register(client)
    response = client.post('/login', json=user)
    assert response.status_code == 200
    return response


def test_logout(client):
    login_response = test_login(client)
    access_token = login_response.json['accessToken']
    headers = authorization_header(access_token)
    response = client.delete('/logout', headers=headers)
    assert response.status_code == 200


def test_refresh_token(client):
    login_response = test_login(client)
    refresh_token = login_response.json['refreshToken']
    headers = authorization_header(refresh_token)
    response = client.post('/refresh-token', headers=headers)
    assert response.status_code == 200


def test_update_email(client):
    login_response = test_login(client)
    access_token = login_response.json['accessToken']
    headers = authorization_header(access_token)
    data = {'email': 'test@example.ba'}
    response = client.put('/update-email', json=data, headers=headers)
    assert response.status_code == 200


def test_update_password(client):
    login_response = test_login(client)
    access_token = login_response.json['accessToken']
    headers = authorization_header(access_token)
    data = {
        'currentPassword': 'password',
        'newPassword': 'newPassword',
        'newPasswordConfirm': 'newPassword'}
    response = client.put('/update-password', json=data, headers=headers)
    assert response.status_code == 200


def test_get_user(client):
    login_response = test_login(client)
    access_token = login_response.json['accessToken']
    headers = authorization_header(access_token)
    response = client.get('/get-user', headers=headers)
    assert response.status_code == 200


def test_delete_user(client):
    login_response = test_login(client)
    access_token = login_response.json['accessToken']
    headers = authorization_header(access_token)
    response = client.delete('/delete-user', headers=headers)
    assert response.status_code == 200
