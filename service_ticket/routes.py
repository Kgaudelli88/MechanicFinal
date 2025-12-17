from app.utils import error_response
from . import service_ticket_bp
from app.db import db

@service_ticket_bp.route('/mechanic-service-ticket/', methods=['GET'])
def get_mechanic_service_tickets():
    sql = db.text('SELECT * FROM mechanic_service_ticket')
    result = db.session.execute(sql)
    assignments = [dict(row._mapping) for row in result]
    return jsonify(assignments), 200


from flask import request, jsonify
from . import service_ticket_bp
from .models import ServiceTicket
from app.db import db








# Create a new Service Ticket

from .schemas import ServiceTicketSchema


@service_ticket_bp.route('/mechanic-service-ticket/', methods=['POST'])
def assign_mechanic_to_ticket():
    data = request.get_json()
    mechanic_id = data.get('mechanic_id')
    service_ticket_id = data.get('service_ticket_id')
    status = data.get('status', 'pending')
    if not mechanic_id or not service_ticket_id:
        return error_response('mechanic_id and service_ticket_id are required.', 400)
    # Direct SQL for association table with status
    sql = db.text('INSERT INTO mechanic_service_ticket (mechanic_id, service_ticket_id, status) VALUES (:mechanic_id, :service_ticket_id, :status)')
    try:
        db.session.execute(sql, {'mechanic_id': mechanic_id, 'service_ticket_id': service_ticket_id, 'status': status})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error assigning mechanic: {str(e)}', 500)
    return {'message': 'Mechanic assigned to service ticket with status.'}, 201

# DELETE a Service Ticket
@service_ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_service_ticket(ticket_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Service ticket deleted', 'ticket_id': ticket.id}), 200
from flask import request, jsonify
from . import service_ticket_bp
from .models import ServiceTicket
from app.db import db


# Update mechanics for a service ticket (add/remove mechanics)
@service_ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_mechanics(ticket_id):
    from .schemas import ServiceTicketSchema
    from mechanic.models import Mechanic
    service_ticket_schema = ServiceTicketSchema()
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    data = request.get_json()
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])
    # Remove mechanics
    for mid in remove_ids:
        mechanic = Mechanic.query.get(mid)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
    # Add mechanics
    for mid in add_ids:
        mechanic = Mechanic.query.get(mid)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200



# Remove a mechanic from a service ticket
@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    from .schemas import ServiceTicketSchema
    from mechanic.models import Mechanic
    service_ticket_schema = ServiceTicketSchema()
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200

# Assign a mechanic to a service ticket
@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    from .schemas import ServiceTicketSchema
    from mechanic.models import Mechanic
    service_ticket_schema = ServiceTicketSchema()
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
    return jsonify(service_ticket_schema.dump(ticket)), 200

@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    from .schemas import ServiceTicketSchema
    service_tickets_schema = ServiceTicketSchema(many=True)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = ServiceTicket.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'service_tickets': service_tickets_schema.dump(pagination.items),
        'total': pagination.total,
    }), 200

# Create a new Service Ticket

from .schemas import ServiceTicketSchema

@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    service_ticket_schema = ServiceTicketSchema()
    data = request.get_json()
    customer_id = data.get('customer_id')
    status = data.get('status', 'pending')
    if not customer_id:
        return error_response('customer_id is required for service ticket.', 400)
    new_ticket = ServiceTicket(
        VIN=data.get('VIN'),
        description=data.get('description'),
        customer_id=customer_id,
        year=data.get('year'),
        make=data.get('make'),
        model=data.get('model'),
        service_date=data.get('service_date')
    )
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify(service_ticket_schema.dump(new_ticket)), 201
