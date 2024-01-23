import os
from dotenv import load_dotenv

load_dotenv('.env')

SQLALCHEMY_DATABASE_URI = 'sqlite:///doctor.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
