from flask import Blueprint, jsonify
from app.extensions import cache

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@cache.cached(timeout=60)
def get_users():
    # Example static response; replace with actual DB query as needed
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
    return jsonify(users)
