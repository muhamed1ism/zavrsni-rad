from tests.test_login import login


def test_get_user(client, headers):
    login(client)
    response = client.get('/get-user', headers=headers)
    assert response.status_code == 200
