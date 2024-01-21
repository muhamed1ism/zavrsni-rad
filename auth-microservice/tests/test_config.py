# test config
from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'test_secret'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
