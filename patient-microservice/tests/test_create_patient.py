from unittest.mock import MagicMock


def create_patient(client, monkeypatch, headers):
    mock_get_user_role = MagicMock(return_value='patient')
    monkeypatch.setattr("app.routes.create_patient.get_user_role", mock_get_user_role)
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'dateOfBirth': '1990-01-01T00:00:00.000Z'
    }
    response = client.post('/create-patient', json=data, headers=headers)
    return response


def test_create_patient(client, monkeypatch, headers):
    response = create_patient(client, monkeypatch, headers)
    assert response.status_code == 201
