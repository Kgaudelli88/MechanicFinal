from app.db import db

mechanic_service_ticket = db.Table(
    'service_mechanics',
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanic.id'))
)
