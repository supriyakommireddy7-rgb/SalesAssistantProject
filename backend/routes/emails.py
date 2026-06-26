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
    try:
        gmail_service = GmailService()
    except Exception as e:
        return jsonify({'message': f'Gmail Authentication Error: {str(e)}'}), 500
        
    gemini_service = GeminiService()
    
    try:
        unread_emails = gmail_service.get_unread_emails()
    except Exception as e:
        return jsonify({'message': f'Error fetching emails: {str(e)}'}), 500
        
    processed_count = 0
    
    for email_data in unread_emails:
        if Email.query.filter_by(gmail_msg_id=email_data['gmail_msg_id']).first():
            continue
            
        # Here we use the strictly parsed email address, but save name if needed.
        # But for backward compatibility we store sender as "Name <email>" if that's what was there.
        # Let's just use the sender_email for filtering, and store the full string in sender
        sender_str = f"{email_data['sender_name']} <{email_data['sender_email']}>" if email_data['sender_name'] != email_data['sender_email'] else email_data['sender_email']
        customer = Customer.query.filter_by(email=email_data['sender_email']).first()
        customer_id = customer.id if customer else None
        
        new_email = Email(
            gmail_thread_id=email_data['gmail_thread_id'],
            gmail_msg_id=email_data['gmail_msg_id'],
            customer_id=customer_id,
            sender=sender_str,
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
            notif = Notification(title="New Human Task", message=f"Email from {sender_str} requires human response.", type="Warning")
            db.session.add(notif)
        else:
            try:
                success = gmail_service.send_reply(
                    email_data['gmail_thread_id'], 
                    email_data['sender_email'], 
                    email_data['subject'], 
                    reply_text,
                    in_reply_to_message_id=email_data.get('message_id')
                )
                if success:
                    new_email.status = 'AI Replied' if reply_type == 'AI' else 'Rule Replied'
                    gmail_service.mark_as_read(email_data['gmail_msg_id'])
            except Exception as e:
                print(f"Failed to send reply or mark as read for {email_data['gmail_msg_id']}: {e}")
                new_email.status = 'Failed to Reply'
            
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
        
    try:
        gmail_service = GmailService()
    except Exception as e:
        return jsonify({'message': f'Gmail Authentication Error: {str(e)}'}), 500
        
    try:
        # Extract plain email if it's in the "Name <email>" format
        import re
        to_email = email.sender
        match = re.match(r"(.*)<(.*)>", email.sender)
        if match:
            to_email = match.group(2).strip()
            
        success = gmail_service.send_reply(
            email.gmail_thread_id, 
            to_email, 
            email.subject, 
            reply_text
        )
        
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
    except Exception as e:
        return jsonify({'message': f'Failed to send reply: {str(e)}'}), 500
        
    return jsonify({'message': 'Failed to send reply'}), 500
