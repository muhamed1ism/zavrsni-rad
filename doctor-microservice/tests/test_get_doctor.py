from tests.test_create_doctor import create_doctor


def test_get_doctor(client, monkeypatch, headers):
    create_doctor(client, monkeypatch, headers)
    response = client.get('/get-doctor', headers=headers)
    assert response.status_code == 200
