from app import app, db

# Create database and tables
with app.app_context():
    db.create_all()
    print("✓ Database created successfully!")
    print("✓ 'leads' table created!")
