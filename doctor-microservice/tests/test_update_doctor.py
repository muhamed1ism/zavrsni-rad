from tests.test_create_doctor import create_doctor


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
