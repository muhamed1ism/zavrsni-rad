from unittest.mock import MagicMock
from tests.test_create_appointment import create_appointment


def approve_appointment(client, monkeypatch, headers):
    mock_get_user_role = MagicMock(return_value='doctor')
    monkeypatch.setattr('app.routes.approve_appointment.get_user_role', mock_get_user_role)
    response = client.put('/appointment/approve/1', headers=headers)
    return response


def test_approve_appointment(client, monkeypatch, headers):
    create_appointment(client, monkeypatch, headers)
    response = approve_appointment(client, monkeypatch, headers)
    assert response.status_code == 200
