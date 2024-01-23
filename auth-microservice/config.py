import os
from datetime import timedelta
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv('.env')

# DATABASE
SQLALCHEMY_DATABASE_URI = 'sqlite:///auth.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
