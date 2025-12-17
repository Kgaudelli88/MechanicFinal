from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import ServiceTicket
from marshmallow import fields

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
    year = fields.Integer(required=False, allow_none=True)
    make = fields.String(required=False, allow_none=True)
    model = fields.String(required=False, allow_none=True)
