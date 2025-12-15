
from . import mechanic_bp
from flask import jsonify
from app.db import db
from .models import Mechanic

# Imports
from flask import request, jsonify
from app.utils import error_response
from . import mechanic_bp
from .models import Mechanic
from app import db
from jose import jwt
from datetime import datetime, timedelta
from app.extensions import limiter
from werkzeug.security import check_password_hash

# Mechanic token encoding
SECRET_KEY = 'your_secret_key'  # Use the same as customer for simplicity
ALGORITHM = 'HS256'
def encode_mechanic_token(mechanic_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
        'sub': mechanic_id,
        'role': 'mechanic'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Mechanic token required decorator
from functools import wraps
def mechanic_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return error_response('Token is missing!', 401)
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if data.get('role') != 'mechanic':
                return error_response('Mechanic token required!', 403)
            mechanic_id = data['sub']
        except Exception as e:
            return error_response('Token is invalid!', 401)
        return f(mechanic_id, *args, **kwargs)
    return decorated

# Mechanic login route
@mechanic_bp.route('/login', methods=['POST'])
@limiter.limit('5 per minute')
def mechanic_login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return error_response('Email and password are required.', 400)
    mechanic = Mechanic.query.filter_by(email=data['email']).first()
    if not mechanic or not check_password_hash(mechanic.password, data['password']):
        return error_response('Invalid credentials', 401)
    token = encode_mechanic_token(mechanic.id)
    return jsonify({'token': token})
# Imports
from flask import request, jsonify
from . import mechanic_bp
from .models import Mechanic
from app import db

# Get mechanics ordered by number of tickets worked on
@mechanic_bp.route('/by-ticket-count', methods=['GET'])
def mechanics_by_ticket_count():
    from .schemas import MechanicSchema
    mechanics_schema = MechanicSchema(many=True)
    from sqlalchemy import func
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    mechanics_query = (
        db.session.query(Mechanic)
        .outerjoin(Mechanic.service_tickets)
        .group_by(Mechanic.id)
        .order_by(func.count().desc())
    )
    pagination = mechanics_query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'mechanics': mechanics_schema.dump(pagination.items),
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    }), 200

# Create a new Mechanic
@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    from .schemas import MechanicSchema
    mechanic_schema = MechanicSchema()
    data = request.get_json()
    # Validate input
    try:
        new_mechanic = mechanic_schema.load(data, session=db.session)
    except Exception as err:
        return error_response(str(err), 400)
    db.session.add(new_mechanic)
    db.session.commit()
    mechanic_data = mechanic_schema.dump(new_mechanic)
    # Ensure id is present in the response
    mechanic_data['id'] = new_mechanic.id
    return jsonify(mechanic_data), 201

@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    from .schemas import MechanicSchema
    mechanics_schema = MechanicSchema(many=True)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Mechanic.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'mechanics': mechanics_schema.dump(pagination.items),
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    }), 200


# Get a specific Mechanic
@mechanic_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    from .schemas import MechanicSchema
    mechanic_schema = MechanicSchema()
    mechanic = Mechanic.query.get_or_404(id)
    return jsonify(mechanic_schema.dump(mechanic)), 200

# Update a Mechanic
@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    from .schemas import MechanicSchema
    mechanic_schema = MechanicSchema()
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()
    mechanic.name = data.get('name', mechanic.name)
    mechanic.specialty = data.get('specialty', mechanic.specialty)
    mechanic.email = data.get('email', mechanic.email)
    mechanic.phone = data.get('phone', mechanic.phone)
    mechanic.salary = data.get('salary', mechanic.salary)
    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic)), 200

# Delete a Mechanic
@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': 'Mechanic deleted'}), 200
