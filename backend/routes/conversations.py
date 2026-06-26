from flask import Blueprint, jsonify
from models import db
from models.conversation import Conversation
from utils.auth_utils import token_required

conversations_bp = Blueprint('conversations', __name__)

@conversations_bp.route('/', methods=['GET'])
@token_required
def get_conversations(current_admin):
    conversations = Conversation.query.order_by(Conversation.date.desc()).all()
    return jsonify([c.to_dict() for c in conversations]), 200

@conversations_bp.route('/<int:email_id>', methods=['GET'])
@token_required
def get_conversation_by_email(current_admin, email_id):
    conversations = Conversation.query.filter_by(email_id=email_id).all()
    return jsonify([c.to_dict() for c in conversations]), 200
