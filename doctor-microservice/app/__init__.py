from flask import Flask

from app.models import db
from app.routes import app_routes, cors, jwt


def create_app(test_config=None):
    # Flask
    app = Flask(__name__)

    # Config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Routes
    app_routes(app)

    # CORS
    cors.init_app(app)

    # JWT
    jwt.init_app(app)

    # Database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
