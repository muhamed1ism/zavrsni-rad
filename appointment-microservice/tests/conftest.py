import os
import pytest
from flask_jwt_extended import create_access_token

from app import create_app, db


@pytest.fixture(autouse=True)
def env_setup():
    os.environ['FLASK_ENV'] = 'testing'
    yield
    os.environ['FLASK_ENV'] = 'development'


@pytest.fixture
def app():
    app = create_app()

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
