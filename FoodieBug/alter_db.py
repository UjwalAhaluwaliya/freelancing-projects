from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE orders ADD COLUMN delivery_partner_id INTEGER DEFAULT NULL;"))
        db.session.execute(text("ALTER TABLE orders ADD CONSTRAINT fk_orders_delivery_partner FOREIGN KEY (delivery_partner_id) REFERENCES users(id);"))
        db.session.commit()
        print("Database altered successfully! Column added.")
    except Exception as e:
        print(f"Error altering database: {e}")
