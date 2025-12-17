from app.db import db
from service_ticket.models import mechanic_service_ticket

class Mechanic(db.Model):
    __tablename__ = 'mechanic'
    id = db.Column(db.Integer, primary_key=True)
    # ...existing fields...
    service_tickets = db.relationship('ServiceTicket', secondary=mechanic_service_ticket, back_populates='mechanics')