from models.customer import Customer
from app.db import db

mechanic_service_ticket = db.Table(
    'mechanic_service_ticket',
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True),
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('status', db.String(50), nullable=False, default='open'),
    extend_existing=True
)

class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"
    id = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    make = db.Column(db.String(50), nullable=True)
    model = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(300), nullable=False)
    service_date = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    customer = db.relationship("Customer", back_populates="service_tickets")
    mechanics = db.relationship("Mechanic", secondary=mechanic_service_ticket, back_populates="service_tickets")

