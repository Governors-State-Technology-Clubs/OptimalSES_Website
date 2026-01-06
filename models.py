from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True) # Optional (contact forms might not have it)
    service = db.Column(db.String(100), nullable=True) # Project type (quote only)
    message = db.Column(db.Text, nullable=False) # Contact message or project details
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Lead id = {self.id} form_type = {self.form_type} name={self.name}>"
