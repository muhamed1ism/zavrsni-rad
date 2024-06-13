from tests.test_login import login


def test_update_password(client, headers):
    login(client)
    data = {
        'currentPassword': 'password',
        'newPassword': 'newPassword',
        'newPasswordConfirm': 'newPassword'}
    response = client.put('/update-password', json=data, headers=headers)
    assert response.status_code == 200
