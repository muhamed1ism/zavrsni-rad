# app config
from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'sqlite:///auth.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'tajni_kljuc'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)