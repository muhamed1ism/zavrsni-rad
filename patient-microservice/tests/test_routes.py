from unittest.mock import MagicMock


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def create_patient(client, monkeypatch, headers):
    mock_requests = MagicMock()
    mock_requests.get.return_value.json.return_value = {'role': 'patient'}
    monkeypatch.setattr("app.routes.requests", mock_requests)
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


def test_get_patient(client, monkeypatch, headers):
    create_patient(client, monkeypatch, headers)
    response = client.get('/get-patient', headers=headers)
    assert response.status_code == 200


def test_update_patient(client, monkeypatch, headers):
    create_patient(client, monkeypatch, headers)
    data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'date_of_birth': '1990-01-01',
        'address': '123 Main St',
        'phone_number': '123-456-7890'
    }
    response = client.put('/update-patient', json=data, headers=headers)
    assert response.status_code == 200


def test_delete_patient(client, monkeypatch, headers):
    create_patient(client, monkeypatch, headers)
    response = client.delete('/delete-patient', headers=headers)
    assert response.status_code == 200
