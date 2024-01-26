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

    def test_create_appointment(self):
        data = {
            'doctor_id': 1,
            'date': '2020-01-01',
            'time': '12:00:00',
            'reason': 'Checkup'
        }

        response = self.client.post('/appointment/create', json=data)

        assert response.status_code == 200
