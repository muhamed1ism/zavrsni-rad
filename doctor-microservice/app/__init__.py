import os
from flask import Flask

from config import DevelopmentConfig, TestingConfig, ProductionConfig
from app.extensions import jwt, cors, db
from app.routes import register_blueprints


def create_app():
    # Flask
    app = Flask(__name__)

    # Configuration
    config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])

    # CORS
    cors.init_app(app)

    # JWT
    jwt.init_app(app)

    # Blueprint
    register_blueprints(app)

    # Database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
