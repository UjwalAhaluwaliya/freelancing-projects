from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import inspect, text
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def _sync_legacy_schema():
    """Apply lightweight schema fixes for older local databases."""
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    if 'orders' not in tables:
        return

    order_columns = {col['name'] for col in inspector.get_columns('orders')}
    if 'delivery_partner_id' not in order_columns:
        db.session.execute(text("ALTER TABLE orders ADD COLUMN delivery_partner_id INT NULL"))
        db.session.commit()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.customer import customer
    from app.routes.delivery import delivery
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(customer, url_prefix='/customer')
    app.register_blueprint(delivery, url_prefix='/delivery')

    with app.app_context():
        db.create_all()
        _sync_legacy_schema()

    @app.cli.command("init-db")
    def init_db_command():
        """Create database tables and seed sample data."""
        with app.app_context():
            db.create_all()
            from app.utils.seed import seed_data
            seed_data()
            print("Database initialized and optionally seeded.")

    return app
