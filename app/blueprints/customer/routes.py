from functools import wraps
from flask import Blueprint, request, jsonify
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.db import db
from models.customer import Customer
from .schemas import CustomerSchema, LoginSchema
from app.utils import error_response
from app.extensions import limiter

SECRET_KEY = 'your_secret_key'  # Use the same key as in your app
ALGORITHM = 'HS256'

customer_bp = Blueprint('customer', __name__)

def token_required(f):
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
            customer_id = data['sub']
        except Exception as e:
            return error_response('Token is invalid!', 401)
        return f(customer_id, *args, **kwargs)
    return decorated

# Add login route after customer_bp is defined
@customer_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return error_response('Email and password are required.', 400)
    customer = Customer.query.filter_by(email=data['email']).first()
    if not customer or customer.password != data['password']:
        return error_response('Invalid credentials', 401)
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),  # expiration time (1 hour from now)
        'iat': datetime.now(timezone.utc),  # issued at
        'sub': str(customer.id)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return jsonify({'token': token})

# Create a new customer (register)
@customer_bp.route('/', methods=['POST'])
@limiter.limit('5 per minute')
def create_customer():
    data = request.get_json()
    schema = CustomerSchema()
    errors = schema.validate(data, session=db.session)
    if errors:
        return error_response(errors, 400)
    for field in ['email', 'password', 'name', 'phone']:
        if not data.get(field):
            return error_response(f"'{field}' is required.", 400)
    if Customer.query.filter_by(email=data['email']).first():
        return error_response('Email already exists.', 400)
    customer = Customer(email=data['email'], password=data['password'], name=data['name'], phone=data['phone'])
    db.session.add(customer)
    db.session.commit()
    return jsonify(schema.dump(customer)), 201

# Get all customers (paginated)
@customer_bp.route('/', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    schema = CustomerSchema(many=True)
    return jsonify({
        'customers': schema.dump(pagination.items),
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    })

# Get a single customer by ID
@customer_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    schema = CustomerSchema()
    return jsonify(schema.dump(customer))

# Update a customer by ID
@customer_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    schema = CustomerSchema(partial=True)
    errors = schema.validate(data, session=db.session)
    if errors:
        return error_response(errors, 400)
    if 'email' in data and data['email'] != customer.email:
        if Customer.query.filter_by(email=data['email']).first():
            return error_response('Email already exists.', 400)
        customer.email = data['email']
    if 'name' in data:
        customer.name = data['name']
    if 'password' in data:
        customer.password = data['password']
    if 'phone' in data:
        customer.phone = data['phone']
    db.session.commit()
    return jsonify(schema.dump(customer))

# Delete a customer by ID (restricted to logged-in customer)
@customer_bp.route('/me', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'})
