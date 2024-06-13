def user():
    return {
        'email': 'test@example.com',
        'password': 'password',
        'passwordConfirm': 'password',
        'role': 'patient'
    }


def register(client):
    response = client.post('/register', json=user())
    return response


def test_register(client):
    response = register(client)
    assert response.status_code == 201
