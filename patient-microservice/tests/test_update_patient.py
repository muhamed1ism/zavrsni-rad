from tests.test_create_patient import create_patient


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
