from app.db import db

class Mechanic(db.Model):
    __tablename__ = "mechanics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(150), unique=True, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    specialty = db.Column(db.String(100), nullable=True)
    service_tickets = db.relationship(
        'ServiceTicket',
        secondary='mechanic_service_ticket',
        back_populates='mechanics'
    )
