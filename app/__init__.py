

from app.logging_utils import setup_logging
from flask import Flask
from app.db import db
from mechanic import mechanic_bp
from service_ticket import service_ticket_bp
import os
try:
    from app.extensions import limiter, cache
except ImportError:
    limiter = None
    cache = None

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_config():
    config_name = os.environ.get('APP_CONFIG', 'DevelopmentConfig')
    try:
        from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
    except ImportError:
        from config import DevelopmentConfig, TestingConfig, ProductionConfig
    configs = {
        'DevelopmentConfig': DevelopmentConfig,
        'TestingConfig': TestingConfig,
        'ProductionConfig': ProductionConfig
    }
    return configs.get(config_name, DevelopmentConfig)


def create_app():
    app = Flask(__name__)
    setup_logging(app)
    app.config.from_object(get_config())
    db.init_app(app)
    if limiter:
        limiter.init_app(app)
    if cache:
        cache.init_app(app)

    # Ensure models are registered with SQLAlchemy before using them
    import mechanic.models
    import service_ticket.models

    from app.blueprints.customer.routes import customer_bp
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(customer_bp, url_prefix='/customers')
    # Add detailed error handler for debugging in CI
    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        response = {
            'message': 'Internal server error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return response, 500
    return app
