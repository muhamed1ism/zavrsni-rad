from tests.test_login import login


def test_update_email(client, headers):
    login(client)
    data = {'email': 'test@example.ba'}
    response = client.put('/update-email', json=data, headers=headers)
    assert response.status_code == 200
