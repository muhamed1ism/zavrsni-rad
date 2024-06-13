from tests.test_register import test_register, user


def login(client):
    test_register(client)
    response = client.post('/login', json=user())
    return response


def test_login(client):
    response = login(client)
    assert response.status_code == 200
