from app import create_app, db

app = create_app()

with app.app_context():
    print("Dropping all tables to clean schema...")
    db.drop_all()
    print("Re-creating all tables with updated schema...")
    db.create_all()
    
    # Optionally seed data back
    from app.utils.seed import seed_data
    seed_data()
    print("Database synced and re-seeded successfully!")
