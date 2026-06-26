from . import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    budget = db.Column(db.String(50), nullable=True)
    preferred_location = db.Column(db.String(100), nullable=True)
    interested_plot = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='New') 
    priority = db.Column(db.String(50), default='Medium') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    emails = db.relationship('Email', backref='customer', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'city': self.city,
            'budget': self.budget,
            'preferred_location': self.preferred_location,
            'interested_plot': self.interested_plot,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
