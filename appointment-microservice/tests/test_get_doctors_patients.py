from unittest.mock import MagicMock
from tests.test_create_appointment import create_appointment
from tests.test_approve_appointment import approve_appointment


def test_get_doctors_patients(client, monkeypatch, headers):
    create_appointment(client, monkeypatch, headers)
    approve_appointment(client, monkeypatch, headers)
    mock_get_jwt_identity = MagicMock(return_value=2)
    mock_get_doctor_id = MagicMock(return_value=1)
    mock_get_patient_date_of_birth = MagicMock(side_effect=['1980-01-01'])
    mock_get_patient_address = MagicMock(side_effect=['Ulica 123'])
    mock_get_patient_phone_number = MagicMock(side_effect=['0612345678'])
    monkeypatch.setattr('app.routes.get_doctors_patients.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_doctors_patients.get_doctor_id', mock_get_doctor_id)
    monkeypatch.setattr('app.routes.get_doctors_patients.get_patient_date_of_birth', mock_get_patient_date_of_birth)
    monkeypatch.setattr('app.routes.get_doctors_patients.get_patient_address', mock_get_patient_address)
    monkeypatch.setattr('app.routes.get_doctors_patients.get_patient_phone_number', mock_get_patient_phone_number)
    response = client.get('/get-doctors-patients', headers=headers)
    assert response.status_code == 200
