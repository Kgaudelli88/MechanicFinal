from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.customer import Customer
from marshmallow import fields, Schema

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
    name = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    phone = fields.String(required=True)

# Use plain Schema for login validation (no DB instance needed)
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
