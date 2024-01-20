from flask_testing import TestCase
from app import app, db


class TestAuth(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['JWT_SECRET_KEY'] = 'test_secret'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.data == b'Welcome to the authentication microservice!'

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
        token = 'Bearer ' + response.get_json()['access_token']
        return token

    def test_logout(self):
        token = self.test_login()
        response = self.client.delete('/logout', headers={'Authorization': token})
        assert response.status_code == 200

    def test_update_email(self):
        token = self.test_login()

        data = {
            'email': 'test@example.ba'
        }

        response = self.client.post('/update-email', headers={'Authorization': token}, json=data)
        assert response.status_code == 200

    def test_update_password(self):
        token = self.test_login()

        data = {
            'current_password': 'password',
            'new_password': 'new_password',
            'new_password_confirm': 'new_password'
        }

        response = self.client.post('/update-password', headers={'Authorization': token}, json=data)
        assert response.status_code == 200

    def test_delete(self):
        token = self.test_login()

        response = self.client.delete('/delete', headers={'Authorization': token})
        assert response.status_code == 200
