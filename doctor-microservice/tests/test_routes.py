from unittest.mock import MagicMock


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def create_doctor(client, monkeypatch, headers):
    mock_requests = MagicMock()
    mock_requests.get.return_value.json.return_value = {'role': 'doctor'}
    monkeypatch.setattr("app.routes.requests", mock_requests)
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


def test_get_doctor(client, monkeypatch, headers):
    create_doctor(client, monkeypatch, headers)
    response = client.get('/get-doctor', headers=headers)
    assert response.status_code == 200


def test_update_doctor(client, monkeypatch, headers):
    create_doctor(client, monkeypatch, headers)
    data = {
        'firstName': 'Jane',
        'lastName': 'Smith',
        'date_of_birth': '1990-02-01',
        'address': '123 Main St',
        'phone_number': '123-456-7890'
    }
    response = client.put('/update-doctor', json=data, headers=headers)
    assert response.status_code == 200


def test_delete_doctor(client, monkeypatch, headers):
    create_doctor(client, monkeypatch, headers)
    response = client.delete('/delete-doctor', headers=headers)
    assert response.status_code == 200
