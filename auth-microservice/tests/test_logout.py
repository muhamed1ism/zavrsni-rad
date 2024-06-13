from tests.test_login import test_login


def test_logout(client, headers):
    test_login(client)
    response = client.delete('/logout', headers=headers)
    assert response.status_code == 200
