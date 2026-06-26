from flask import Blueprint, request, jsonify
from models import db
from models.email import Email
from models.customer import Customer
from models.conversation import Conversation
from models.notification import Notification
from services.gmail_service import GmailService
from services.gemini_service import GeminiService
from services.rule_engine import RuleEngine
from utils.auth_utils import token_required

emails_bp = Blueprint('emails', __name__)

@emails_bp.route('/', methods=['GET'])
@token_required
def get_emails(current_admin):
    emails = Email.query.order_by(Email.date.desc()).all()
    return jsonify([e.to_dict() for e in emails]), 200

@emails_bp.route('/sync', methods=['POST'])
@token_required
def sync_emails(current_admin):
    gmail_service = GmailService()
    gemini_service = GeminiService()
    
    unread_emails = gmail_service.get_unread_emails()
    processed_count = 0
    
    for email_data in unread_emails:
        if Email.query.filter_by(gmail_msg_id=email_data['gmail_msg_id']).first():
            continue
            
        customer = Customer.query.filter_by(email=email_data['sender']).first()
        customer_id = customer.id if customer else None
        
        new_email = Email(
            gmail_thread_id=email_data['gmail_thread_id'],
            gmail_msg_id=email_data['gmail_msg_id'],
            customer_id=customer_id,
            sender=email_data['sender'],
            subject=email_data['subject'],
            body=email_data['body']
        )
        db.session.add(new_email)
        db.session.flush() 
        
        reply_text, confidence = gemini_service.generate_reply(email_data['body'])
        reply_type = 'AI'
        
        if not reply_text or confidence < 0.6:
            reply_text = RuleEngine.get_fallback_reply(email_data['body'])
            reply_type = 'Rule-Based' if reply_text else 'Human'
            
        if reply_type == 'Human':
            new_email.status = 'Awaiting Human Response'
            notif = Notification(title="New Human Task", message=f"Email from {email_data['sender']} requires human response.", type="Warning")
            db.session.add(notif)
        else:
            success = gmail_service.send_reply(
                email_data['gmail_thread_id'], 
                email_data['sender'], 
                email_data['subject'], 
                reply_text
            )
            if success:
                new_email.status = 'AI Replied' if reply_type == 'AI' else 'Rule Replied'
                gmail_service.mark_as_read(email_data['gmail_msg_id'])
            
            conv = Conversation(
                email_id=new_email.id,
                reply_text=reply_text,
                reply_type=reply_type,
                confidence_score=confidence
            )
            db.session.add(conv)
            
        processed_count += 1
        
    db.session.commit()
    return jsonify({'message': f'Synced {processed_count} emails'}), 200

@emails_bp.route('/<int:id>/reply', methods=['POST'])
@token_required
def human_reply(current_admin, id):
    email = Email.query.get_or_404(id)
    data = request.get_json()
    reply_text = data.get('reply_text')
    
    if not reply_text:
        return jsonify({'message': 'Reply text is required'}), 400
        
    gmail_service = GmailService()
    success = gmail_service.send_reply(email.gmail_thread_id, email.sender, email.subject, reply_text)
    
    if success:
        email.status = 'Human Replied'
        conv = Conversation(
            email_id=email.id,
            reply_text=reply_text,
            reply_type='Human',
            confidence_score=1.0
        )
        db.session.add(conv)
        gmail_service.mark_as_read(email.gmail_msg_id)
        db.session.commit()
        return jsonify({'message': 'Reply sent successfully'}), 200
        
    return jsonify({'message': 'Failed to send reply'}), 500
