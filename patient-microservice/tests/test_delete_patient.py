from tests.test_create_patient import create_patient


def test_delete_patient(client, monkeypatch, headers):
    create_patient(client, monkeypatch, headers)
    response = client.delete('/delete-patient', headers=headers)
    assert response.status_code == 200
