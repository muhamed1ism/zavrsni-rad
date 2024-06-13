from flask import Flask

from app.extensions import jwt
from app.models.user import User
from app import db


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return db.session.query(User).filter_by(id=identity).one_or_none()


def register_blueprints(app: Flask):
    from app.routes.home import home_bp
    from app.routes.register import register_bp
    from app.routes.login import login_bp
    from app.routes.logout import logout_bp
    from app.routes.refresh_token import refresh_token_bp
    from app.routes.token_status import token_status_bp
    from app.routes.exchange_refresh import exchange_refresh_bp
    from app.routes.get_user import get_user_bp
    from app.routes.update_email import update_email_bp
    from app.routes.update_password import update_password_bp
    from app.routes.delete_user import delete_user_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(refresh_token_bp)
    app.register_blueprint(token_status_bp)
    app.register_blueprint(exchange_refresh_bp)
    app.register_blueprint(get_user_bp)
    app.register_blueprint(update_email_bp)
    app.register_blueprint(update_password_bp)
    app.register_blueprint(delete_user_bp)
