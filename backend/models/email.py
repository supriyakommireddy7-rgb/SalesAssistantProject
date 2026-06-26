from . import db
from datetime import datetime

class Email(db.Model):
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    gmail_thread_id = db.Column(db.String(100), nullable=True)
    gmail_msg_id = db.Column(db.String(100), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    sender = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255), nullable=True)
    body = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Unread') 

    conversations = db.relationship('Conversation', backref='email_ref', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'gmail_thread_id': self.gmail_thread_id,
            'gmail_msg_id': self.gmail_msg_id,
            'customer_id': self.customer_id,
            'sender': self.sender,
            'subject': self.subject,
            'body': self.body,
            'date': self.date.isoformat(),
            'status': self.status
        }
