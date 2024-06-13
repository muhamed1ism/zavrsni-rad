from datetime import datetime

from app import db


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    patient_name = db.Column(db.String(50), nullable=False)
    doctor_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(50), default='na čekanju', nullable=False)

    def __repr__(self):
        return f'<Appointment {self.patient_id} {self.doctor_id} {self.date} {self.time} {self.status}>'


    def save(self):
        db.session.add(self)
        db.session.commit()
