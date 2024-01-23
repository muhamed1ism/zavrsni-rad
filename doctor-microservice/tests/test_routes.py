from flask_testing import TestCase
from app import app, db


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

    def test_create_profile(self):
        from flask_jwt_extended import create_access_token

        access_token = create_access_token(identity=1)
        headers = {'Authorization': 'Bearer ' + access_token}

        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'address': '123 Main St',
            'phone_number': '123-456-7890'
        }

        response = self.client.post(
            '/profile/create',
            json=data,
            headers=headers
        )

        assert response.status_code == 200
        return headers

    def test_get_profile(self):
        headers = self.test_create_profile()

        response = self.client.get(
            '/profile',
            headers=headers
        )

        assert response.status_code == 200
        assert response.json['first_name'] == 'John'
        return response

    def test_update_profile(self):
        headers = self.test_create_profile()

        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'address': '123 Main St',
            'phone_number': '123-456-7890'
        }

        response = self.client.put(
            '/profile/update',
            json=data,
            headers=headers
        )

        assert response.status_code == 200

        get_response = self.client.get(
            '/profile',
            headers=headers
        )

        assert get_response.status_code == 200
        assert get_response.json['first_name'] == 'Jane'

    def test_delete_profile(self):
        headers = self.test_create_profile()

        response = self.client.delete(
            '/profile/delete',
            headers=headers
        )

        assert response.status_code == 200

        get_response = self.client.get(
            '/profile',
            headers=headers
        )

        assert get_response.status_code == 404
