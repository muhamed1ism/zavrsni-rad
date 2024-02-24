import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.models import db


class TestingConfig:
    TESTING = True

    # DATABASE
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = 'b0e8a53a216be2ec1308128e'


app = create_app(TestingConfig.__dict__)


@pytest.fixture
def client():
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def headers():
    with app.app_context():
        access_token = create_access_token(identity=1)
    return {'Authorization': 'Bearer ' + access_token}