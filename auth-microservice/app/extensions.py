from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask import Blueprint

# SQLAlchemy
db = SQLAlchemy()

# CORS
cors = CORS()

# JWT
jwt = JWTManager()

# Bcrypt
bcrypt = Bcrypt()

# Blueprint
bp = Blueprint('routes', __name__)
