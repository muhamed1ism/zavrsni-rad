import pytest
from unittest.mock import MagicMock
from flask_jwt_extended import create_access_token

import tests.test_config as test_config
from app.models import db
from app import create_app


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


@pytest.fixture
def headers():
    with app.app_context():
        access_token = create_access_token(identity=1)
    return {'Authorization': 'Bearer ' + access_token}


def create_appointment(client, monkeypatch, headers):
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_patient_id = MagicMock(return_value=1)
    mock_get_patient_name = MagicMock(return_value='John Doe')
    mock_get_doctor_name = MagicMock(return_value='Dr. Smith')
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_patient_id', mock_get_patient_id)
    monkeypatch.setattr('app.routes.get_patient_name', mock_get_patient_name)
    monkeypatch.setattr('app.routes.get_doctor_name', mock_get_doctor_name)
    new_appointment = {
        'doctorId': 1,
        'date': '2024-04-01T00:00:00.000Z',
        'time': {'hours': '09', 'minutes': '00'},
    }
    response = client.post('/create-appointment', json=new_appointment, headers=headers)
    return response


def test_create_appointment(client, monkeypatch, headers):
    response = create_appointment(client, monkeypatch, headers)
    assert response.status_code == 201


def test_get_all_appointments_for_patient(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='patient')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_patient_id = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_patient_id', mock_get_patient_id)
    response = client.get('/get-all-appointments', headers=headers)
    assert response.status_code == 200
    assert response.json[0]['doctorName'] == 'Dr. Smith'
    assert response.json[0]['patientName'] == 'John Doe'


def test_get_all_appontments_for_doctor(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='doctor')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_doctor_id = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_doctor_id', mock_get_doctor_id)
    response = client.get('/get-all-appointments', headers=headers)
    assert response.status_code == 200
    assert response.json[0]['doctorName'] == 'Dr. Smith'
    assert response.json[0]['patientName'] == 'John Doe'


def test_get_appointment_by_id_for_patient(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='patient')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_patient_id = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_patient_id', mock_get_patient_id)
    response = client.get('/get-appointment/1', headers=headers)
    assert response.status_code == 200
    assert response.json['doctorName'] == 'Dr. Smith'
    assert response.json['patientName'] == 'John Doe'


def test_get_appointment_by_id_for_doctor(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='doctor')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_doctor = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_doctor', mock_get_doctor)
    response = client.get('/get-appointment/1', headers=headers)
    assert response.status_code == 200
    assert response.json['doctorName'] == 'Dr. Smith'
    assert response.json['patientName'] == 'John Doe'


def approve_appointment(client, monkeypatch, headers):
    mock_get_user_role = MagicMock(return_value='doctor')
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    response = client.put('/appointment/approve/1', headers=headers)
    return response


def test_approve_appointment(client, monkeypatch, headers):
    create_appointment(client, monkeypatch, headers)
    response = approve_appointment(client, monkeypatch, headers)
    assert response.status_code == 200


def reject_appointment(client, monkeypatch, headers):
    mock_get_user_role = MagicMock(return_value='doctor')
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    response = client.put('/appointment/reject/1', headers=headers)
    return response


def test_reject_appointment(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    response = reject_appointment(client, monkeypatch, headers)
    assert response.status_code == 200


def cancel_appointment(client, monkeypatch, headers):
    mock_get_user_role = MagicMock(return_value='patient')
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    response = client.put('/appointment/cancel/1', headers=headers)
    return response


def test_cancel_appointment(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    response = cancel_appointment(client, monkeypatch, headers)
    assert response.status_code == 200


def test_restore_appointment(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    response = cancel_appointment(client, monkeypatch, headers)
    assert response.status_code == 200
    response = client.put('/appointment/restore/1', headers=headers)
    assert response.status_code == 200


def test_get_doctors_patients(client, monkeypatch, headers):
    create_appointment(client, monkeypatch, headers)
    approve_appointment(client, monkeypatch, headers)
    mock_get_jwt_identity = MagicMock(return_value=2)
    mock_get_doctor_id = MagicMock(return_value=1)
    mock_get_patient_date_of_birth = MagicMock(side_effect=['1980-01-01'])
    mock_get_patient_address = MagicMock(side_effect=['Ulica 123'])
    mock_get_patient_phone_number = MagicMock(side_effect=['0612345678'])
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_doctor_id', mock_get_doctor_id)
    monkeypatch.setattr('app.routes.get_patient_date_of_birth', mock_get_patient_date_of_birth)
    monkeypatch.setattr('app.routes.get_patient_address', mock_get_patient_address)
    monkeypatch.setattr('app.routes.get_patient_phone_number', mock_get_patient_phone_number)
    response = client.get('/get-doctors-patients', headers=headers)
    assert response.status_code == 200


def test_count_approved_appointments(client, monkeypatch, headers):
    create_appointment(client, monkeypatch, headers)
    approve_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='doctor')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_doctor_id = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_doctor_id', mock_get_doctor_id)
    response = client.get('/appointment/count-approved', headers=headers)
    assert response.status_code == 200
    assert response.json == 1


def test_count_rejected_appointments(client, monkeypatch, headers):
    create_appointment(client, monkeypatch, headers)
    reject_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='doctor')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_doctor_id = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_doctor_id', mock_get_doctor_id)
    response = client.get('/appointment/count-rejected', headers=headers)
    assert response.status_code == 200
    assert response.json == 1


def test_count_pending_appointments(client, monkeypatch, headers):
    create_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='doctor')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_doctor_id = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_doctor_id', mock_get_doctor_id)
    response = client.get('/appointment/count-pending', headers=headers)
    assert response.status_code == 200
    assert response.json == 1
