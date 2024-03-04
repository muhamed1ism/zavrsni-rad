import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.models import db


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'b0e8a53a216be2ec1308128e'
    })

    with app.app_context():
        db.create_all()

    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def headers(app):
    with app.app_context():
        access_token = create_access_token(identity=1)
    return {'Authorization': 'Bearer ' + access_token}
