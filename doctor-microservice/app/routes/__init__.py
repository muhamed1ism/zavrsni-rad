from flask import Flask

from app import db, jwt
from app.models.doctor import Doctor


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    doctor = db.session.query(Doctor).filter_by(user_id=identity).one_or_none()
    return doctor if doctor is not None else {}


def register_blueprints(app: Flask):
    from app.routes.home import home_bp
    from app.routes.create_doctor import create_doctor_bp
    from app.routes.update_doctor import update_doctor_bp
    from app.routes.get_doctor import get_doctor_bp
    from app.routes.get_doctor_by_doctor_id import get_doctor_by_doctor_id_bp
    from app.routes.get_all_doctors import get_all_doctors_bp
    from app.routes.delete_doctor import delete_doctor_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(create_doctor_bp)
    app.register_blueprint(update_doctor_bp)
    app.register_blueprint(get_doctor_bp)
    app.register_blueprint(get_doctor_by_doctor_id_bp)
    app.register_blueprint(get_all_doctors_bp)
    app.register_blueprint(delete_doctor_bp)
