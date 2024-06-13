from unittest.mock import MagicMock
from tests.test_create_appointment import test_create_appointment


def test_get_all_appointments_for_patient(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='patient')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_patient_id = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_all_appointments.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_all_appointments.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_all_appointments.get_patient_id', mock_get_patient_id)
    response = client.get('/get-all-appointments', headers=headers)
    assert response.status_code == 200
    assert response.json[0]['doctorName'] == 'Dr. Smith'
    assert response.json[0]['patientName'] == 'John Doe'
