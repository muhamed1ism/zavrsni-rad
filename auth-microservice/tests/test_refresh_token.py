from tests.test_login import login


def test_refresh_token(client):
    login_response = login(client)
    refresh_token = login_response.json['refreshToken']
    headers = {'Authorization': f'Bearer {refresh_token}'}
    response = client.post('/refresh-token', headers=headers)
    assert response.status_code == 200
