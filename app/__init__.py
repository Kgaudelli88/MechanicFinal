from app.logging_utils import setup_logging

from flask import Flask
from app.db import db
from mechanic import mechanic_bp
from service_ticket import service_ticket_bp
try:
    from app.extensions import limiter, cache
except ImportError:
    limiter = None
    cache = None


def create_app():
    app = Flask(__name__)
    setup_logging(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Trinity2010@localhost/mechanic_shop'
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

    return app
