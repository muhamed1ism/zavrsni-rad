from unittest.mock import MagicMock
from tests.test_create_appointment import test_create_appointment


def cancel_appointment(client, monkeypatch, headers):
    mock_get_user_role = MagicMock(return_value='patient')
    monkeypatch.setattr('app.routes.cancel_appointment.get_user_role', mock_get_user_role)
    response = client.put('/appointment/cancel/1', headers=headers)
    return response


def test_cancel_appointment(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    response = cancel_appointment(client, monkeypatch, headers)
    assert response.status_code == 200
