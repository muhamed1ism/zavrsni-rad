from unittest.mock import MagicMock
from tests.test_create_appointment import test_create_appointment
from tests.test_cancel_appointment import cancel_appointment


def test_restore_appointment(client, monkeypatch, headers):
    test_create_appointment(client, monkeypatch, headers)
    response = cancel_appointment(client, monkeypatch, headers)
    assert response.status_code == 200
    mock_get_user_role = MagicMock(return_value='patient')
    monkeypatch.setattr('app.routes.restore_appointment.get_user_role', mock_get_user_role)
    response = client.put('/appointment/restore/1', headers=headers)
    assert response.status_code == 200
