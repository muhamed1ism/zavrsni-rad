from unittest.mock import MagicMock
from tests.test_create_appointment import create_appointment
from tests.test_reject_appointment import reject_appointment


def test_count_rejected_appointments(client, monkeypatch, headers):
    create_appointment(client, monkeypatch, headers)
    reject_appointment(client, monkeypatch, headers)
    mock_get_user_role = MagicMock(return_value='doctor')
    mock_get_jwt_identity = MagicMock(return_value=1)
    mock_get_doctor_id = MagicMock(return_value=1)
    monkeypatch.setattr('app.routes.count_rejected.get_user_role', mock_get_user_role)
    monkeypatch.setattr('app.routes.count_rejected.get_jwt_identity', mock_get_jwt_identity)
    monkeypatch.setattr('app.routes.count_rejected.get_doctor_id', mock_get_doctor_id)
    response = client.get('/appointment/count-rejected', headers=headers)
    assert response.status_code == 200
    assert response.json == 1
