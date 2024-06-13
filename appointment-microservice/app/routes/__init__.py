from flask import Flask


def register_blueprints(app: Flask):
    from app.routes.home import home_bp
    from app.routes.get_all_appointments import get_all_appointments_bp
    from app.routes.get_appointment_by_id import get_appointment_by_id_bp
    from app.routes.get_doctors_patients import get_doctors_patients_bp
    from app.routes.create_appointment import create_appointment_bp
    from app.routes.approve_appointment import approve_appointment_bp
    from app.routes.cancel_appointment import cancel_appointment_bp
    from app.routes.reject_appointment import reject_appointment_bp
    from app.routes.restore_appointment import restore_appointment_bp
    from app.routes.count_approved import count_approved_bp
    from app.routes.count_pending import count_pending_bp
    from app.routes.count_rejected import count_rejected_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(get_all_appointments_bp)
    app.register_blueprint(get_appointment_by_id_bp)
    app.register_blueprint(get_doctors_patients_bp)
    app.register_blueprint(create_appointment_bp)
    app.register_blueprint(approve_appointment_bp)
    app.register_blueprint(cancel_appointment_bp)
    app.register_blueprint(reject_appointment_bp)
    app.register_blueprint(restore_appointment_bp)
    app.register_blueprint(count_approved_bp)
    app.register_blueprint(count_pending_bp)
    app.register_blueprint(count_rejected_bp)
