from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_argon2 import Argon2
from flask import Blueprint

# SQLAlchemy
db = SQLAlchemy()

# CORS
cors = CORS()

# JWT
jwt = JWTManager()

# Argon2
argon2 = Argon2()

# Blueprint
bp = Blueprint('routes', __name__)
