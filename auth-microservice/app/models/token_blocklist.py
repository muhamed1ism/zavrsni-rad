from sqlalchemy import func
from flask_jwt_extended import get_current_user

from app import db


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

    def __init__(self, jti, type, created_at):
        self.jti = jti
        self.type = type
        self.created_at = created_at
        

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
