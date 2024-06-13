from flask import Flask

from app import db, jwt
from app.models.patient import Patient


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    patient = db.session.query(Patient).filter_by(user_id=identity).one_or_none()
    return patient if patient is not None else {}


def register_blueprints(app: Flask):
    from app.routes.home import home_bp
    from app.routes.create_patient import create_patient_bp
    from app.routes.update_patient import update_patient_bp
    from app.routes.get_patient import get_patient_bp
    from app.routes.get_patient_by_patient_id import get_patient_by_patient_id_bp
    from app.routes.delete_patient import delete_patient_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(create_patient_bp)
    app.register_blueprint(update_patient_bp)
    app.register_blueprint(get_patient_bp)
    app.register_blueprint(get_patient_by_patient_id_bp)
    app.register_blueprint(delete_patient_bp)
