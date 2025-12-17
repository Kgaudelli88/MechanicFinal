import logging
from flask import request

def setup_logging(app):
    # Removed duplicate import
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    @app.before_request
    def log_request_info():
        app.logger.info(f"Request: {request.method} {request.path} | IP: {request.remote_addr} | Data: {request.get_json(silent=True)}")

    @app.errorhandler(Exception)
    def log_error(e):
        app.logger.error(f"Error: {str(e)}", exc_info=True)
        return {'message': 'Internal server error'}, 500










