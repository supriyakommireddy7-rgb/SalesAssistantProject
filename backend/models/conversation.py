from . import db
from datetime import datetime

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey('emails.id'), nullable=False)
    reply_text = db.Column(db.Text, nullable=False)
    reply_type = db.Column(db.String(50), nullable=False) # AI, Rule-Based, Human
    confidence_score = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email_id': self.email_id,
            'reply_text': self.reply_text,
            'reply_type': self.reply_type,
            'confidence_score': self.confidence_score,
            'date': self.date.isoformat()
        }
