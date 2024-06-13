from tests.test_login import login


def test_delete_user(client, headers):
    login(client)
    response = client.delete('/delete-user', headers=headers)
    assert response.status_code == 200
