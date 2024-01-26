from flask_testing import TestCase
from app import app, db


def authorization_header(token):
    return {'Authorization': 'Bearer ' + token}


class TestAuth(TestCase):
    def create_app(self):
        app.config.from_object('test_config')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_register(self):
        data = {
            'email': 'test@example.com',
            'password': 'password',
            'password_confirm': 'password'
        }

        response = self.client.post('/register', json=data)
        assert response.status_code == 200

    def test_login(self):
        self.test_register()

        data = {
            'email': 'test@example.com',
            'password': 'password'
        }

        response = self.client.post('/login', json=data)
        assert response.status_code == 200
        return response

    def test_logout(self):
        login_response = self.test_login()
        access_token = login_response.json['access_token']
        response = self.client.delete('/logout', headers=authorization_header(access_token))
        assert response.status_code == 200

    def test_refresh(self):
        login_response = self.test_login()
        refresh_token = login_response.json['refresh_token']
        response = self.client.post('/refresh', headers=authorization_header(refresh_token))
        assert response.status_code == 200

    def test_update_email(self):
        login_response = self.test_login()
        access_token = login_response.json['access_token']

        data = {
            'email': 'test@example.ba'
        }

        response = self.client.put('/update-email', headers=authorization_header(access_token), json=data)
        assert response.status_code == 200

    def test_update_password(self):
        login_response = self.test_login()
        access_token = login_response.json['access_token']

        data = {
            'current_password': 'password',
            'new_password': 'new_password',
            'new_password_confirm': 'new_password'
        }

        response = self.client.put('/update-password', headers=authorization_header(access_token), json=data)
        assert response.status_code == 200

    def test_delete(self):
        login_response = self.test_login()
        access_token = login_response.json['access_token']

        response = self.client.delete('/delete', headers=authorization_header(access_token))
        assert response.status_code == 200
