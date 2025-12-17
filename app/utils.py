from flask import jsonify

def error_response(message, status_code=400):
    return jsonify({'message': message}), status_code
