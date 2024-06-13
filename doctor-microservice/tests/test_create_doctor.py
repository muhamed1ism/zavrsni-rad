from unittest.mock import MagicMock


def create_doctor(client, monkeypatch, headers):
    mock_get_user_role = MagicMock(return_value='doctor')
    monkeypatch.setattr("app.routes.create_doctor.get_user_role", mock_get_user_role)
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'specialty': 'General Practitioner',
        'dateOfBirth': '1990-01-01T00:00:00.000Z'
    }
    response = client.post('/create-doctor', json=data, headers=headers)
    return response


def test_create_doctor(client, monkeypatch, headers):
    response = create_doctor(client, monkeypatch, headers)
    assert response.status_code == 201
