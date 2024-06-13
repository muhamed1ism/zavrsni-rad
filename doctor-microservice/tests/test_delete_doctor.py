from tests.test_create_doctor import create_doctor


def test_delete_doctor(client, monkeypatch, headers):
    create_doctor(client, monkeypatch, headers)
    response = client.delete('/delete-doctor', headers=headers)
    assert response.status_code == 200
