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
    assert response.data == b'Welcome to the patient microservice!'


def test_create_patient(client):
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'date_of_birth': '1990-01-01',
        'address': '123 Main Street',
        'phone_number': '123-456-7890'
    }

    response = client.post('/create-patient/1', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_update_patient_first_name(client):
    test_create_patient(client)
    data = {'first_name': 'Johnny'}
    response = client.post('/update-patient/1', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_update_patient_last_name(client):
    test_create_patient(client)
    data = {'last_name': 'Donny'}
    response = client.post('/update-patient/1', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_update_patient_date_of_birth(client):
    test_create_patient(client)
    data = {'date_of_birth': '1990-01-02'}
    response = client.post('/update-patient/1', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_update_patient_address(client):
    test_create_patient(client)
    data = {'address': '456 Main Street'}
    response = client.post('/update-patient/1', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_update_patient_phone_number(client):
    test_create_patient(client)
    data = {'phone_number': '123-456-7891'}
    response = client.post('/update-patient/1', json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'


def test_delete_patient(client):
    test_create_patient(client)
    response = client.post('/delete-patient/1')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
