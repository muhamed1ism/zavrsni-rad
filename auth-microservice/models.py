from flask_jwt_extended import get_current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import func

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    role = db.Column(db.String(50), default='patient', nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey('user.id'),
        default=lambda: get_current_user().id,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False
        )

    def __repr__(self):
        return f'<TokenBlocklist jti={self.jti} type={self.type}>'
