from unittest.mock import MagicMock
from tests.test_create_appointment import test_create_appointment


def reject_appointment(client, monkeypatch, headers):
    mock_get_user_role = MagicMock(return_value='doctor')
    monkeypatch.setattr('app.routes.reject_appointment.get_user_role', mock_get_user_role)
    response = client.put('/appointment/reject/1', headers=headers)
    return response


def test_reject_appointment(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    response = reject_appointment(client, monkeypatch, headers)
    assert response.status_code == 200
