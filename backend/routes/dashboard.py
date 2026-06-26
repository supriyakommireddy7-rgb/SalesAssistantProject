from flask import Blueprint, jsonify
from models.customer import Customer
from models.email import Email
from models.conversation import Conversation
from models.notification import Notification
from utils.auth_utils import token_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@token_required
def get_stats(current_admin):
    total_customers = Customer.query.count()
    total_emails = Email.query.count()
    
    ai_replies = Conversation.query.filter_by(reply_type='AI').count()
    rule_replies = Conversation.query.filter_by(reply_type='Rule-Based').count()
    human_pending = Email.query.filter_by(status='Awaiting Human Response').count()
    
    recent_customers = Customer.query.order_by(Customer.created_at.desc()).limit(5).all()
    recent_emails = Email.query.order_by(Email.date.desc()).limit(5).all()
    notifications = Notification.query.order_by(Notification.created_at.desc()).limit(5).all()
    
    return jsonify({
        'total_customers': total_customers,
        'total_emails': total_emails,
        'ai_replies': ai_replies,
        'rule_replies': rule_replies,
        'human_pending': human_pending,
        'recent_customers': [c.to_dict() for c in recent_customers],
        'recent_emails': [e.to_dict() for e in recent_emails],
        'notifications': [n.to_dict() for n in notifications]
    }), 200
