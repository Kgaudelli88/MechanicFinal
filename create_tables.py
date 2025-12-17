from app import create_app
from app.db import db

app = create_app()
with app.app_context():
    #db.drop_all()
    db.create_all()
    print('All tables created successfully.')
    # Print tables for CI debugging
    tables = db.engine.table_names() if hasattr(db.engine, 'table_names') else db.inspect(db.engine).get_table_names()
    print('Tables in database:', tables)
