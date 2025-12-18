

from app.logging_utils import setup_logging
from flasgger import Swagger
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
    from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
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

    # Add Swagger UI at /api/docs/ with required 'specs' key
    # Ensure 'headers' key is always present in Swagger config
    swagger_config = {
        "specs_route": "/api/docs/",
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/api/docs/apispec_1.json',
                "rule_filter": lambda rule: True,  # all endpoints
                "model_filter": lambda tag: True,  # all models
            }
        ],
        "headers": [],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "swagger_ui_bundle_js": "/flasgger_static/swagger-ui-bundle.js",
        "swagger_ui_standalone_preset_js": "/flasgger_static/swagger-ui-standalone-preset.js",
        "swagger_ui_css": "/flasgger_static/swagger-ui.css",
        "jquery_js": "/flasgger_static/lib/jquery.min.js"
    }
    if "headers" not in swagger_config or swagger_config["headers"] is None:
        swagger_config["headers"] = []
    Swagger(app, config=swagger_config)

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
