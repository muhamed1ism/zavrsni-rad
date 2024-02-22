from flask import Flask

from app.models import db
from app.extensions import jwt, cors, bp
from app import routes


def create_app(test_config=None):
    # Flask
    app = Flask(__name__)

    # Config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # CORS
    cors.init_app(app)

    # JWT
    jwt.init_app(app)

    # Blueprint
    app.register_blueprint(bp)

    # Database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
