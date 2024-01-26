from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(25), nullable=False)
    time = db.Column(db.String(25), nullable=False)
    patient_name = db.Column(db.String(50), nullable=False)
    doctor_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    status = db.Column(db.String(50), default='pending', nullable=False)

    def __repr__(self):
        return f'<Appointment {self.patient_id} {self.doctor_id} {self.date} {self.time} {self.status}>'
