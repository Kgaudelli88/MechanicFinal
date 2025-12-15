from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Mechanic

class MechanicSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Mechanic
		load_instance = True
