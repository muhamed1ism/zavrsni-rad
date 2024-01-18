from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from datetime import date

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.String(25), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    last_login = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<User {self.email}>'
