import pytest
from datetime import timedelta
from app import create_app
from app.models import db


class TestingConfig:
    TESTING = True

    # DATABASE
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = 'b0e8a53a216be2ec1308128e'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


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
