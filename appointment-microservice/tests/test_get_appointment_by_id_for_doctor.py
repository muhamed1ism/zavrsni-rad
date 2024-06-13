from unittest.mock import MagicMock
from tests.test_create_appointment import test_create_appointment


def test_get_appointment_by_id_for_doctor(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='doctor')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_doctor = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.get_appointment_by_id.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.get_appointment_by_id.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.get_appointment_by_id.get_doctor_by_user_id', mock_get_doctor)
    response = client.get('/get-appointment/1', headers=headers)
    assert response.status_code == 200
    assert response.json['doctorName'] == 'Dr. Smith'
    assert response.json['patientName'] == 'John Doe'
