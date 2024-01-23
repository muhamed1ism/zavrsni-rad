# test config
import os
from datetime import timedelta
from dotenv import load_dotenv


SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False
if load_dotenv('.test.env'):
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
