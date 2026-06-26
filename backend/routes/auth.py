from flask import Blueprint, request, jsonify
from models import db
from models.admin import Admin
import bcrypt
import jwt
import datetime
from config import Config
from utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Could not verify'}), 401
        
    admin = Admin.query.filter_by(username=data.get('username')).first()
    
    if not admin:
        return jsonify({'message': 'Admin not found'}), 404
        
    if bcrypt.checkpw(data.get('password').encode('utf-8'), admin.password_hash.encode('utf-8')):
        token = jwt.encode({
            'admin_id': admin.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, Config.SECRET_KEY, algorithm="HS256")
        
        return jsonify({'token': token, 'admin': admin.to_dict()}), 200
        
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_admin):
    return jsonify(current_admin.to_dict()), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    # Only for initial setup!
    data = request.get_json()
    if Admin.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'Admin already exists'}), 409
        
    hashed_pw = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt())
    new_admin = Admin(username=data.get('username'), password_hash=hashed_pw.decode('utf-8'))
    
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({'message': 'Admin created successfully'}), 201
