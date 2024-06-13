from tests.test_create_patient import create_patient


def test_get_patient(client, monkeypatch, headers):
    create_patient(client, monkeypatch, headers)
    response = client.get('/get-patient', headers=headers)
    assert response.status_code == 200
