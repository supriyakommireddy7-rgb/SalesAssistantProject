from flask import Blueprint, request, jsonify
from models import db
from models.knowledge_base import KnowledgeBase
from utils.auth_utils import token_required

kb_bp = Blueprint('kb', __name__)

@kb_bp.route('/', methods=['GET'])
@token_required
def get_kb(current_admin):
    kbs = KnowledgeBase.query.all()
    return jsonify([k.to_dict() for k in kbs]), 200

@kb_bp.route('/', methods=['POST'])
@token_required
def create_kb(current_admin):
    data = request.get_json()
    new_kb = KnowledgeBase(
        question=data.get('question'),
        answer=data.get('answer'),
        category=data.get('category'),
        keywords=data.get('keywords'),
        status=data.get('status', 'Active')
    )
    db.session.add(new_kb)
    db.session.commit()
    return jsonify(new_kb.to_dict()), 201

@kb_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_kb(current_admin, id):
    kb = KnowledgeBase.query.get_or_404(id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(kb, key) and key != 'id':
            setattr(kb, key, value)
            
    db.session.commit()
    return jsonify(kb.to_dict()), 200

@kb_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_kb(current_admin, id):
    kb = KnowledgeBase.query.get_or_404(id)
    db.session.delete(kb)
    db.session.commit()
    return jsonify({'message': 'FAQ deleted'}), 200
