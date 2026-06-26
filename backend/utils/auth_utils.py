from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from models.admin import Admin

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
                
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_admin = Admin.query.filter_by(id=data['admin_id']).first()
            if not current_admin:
                raise Exception("Admin not found")
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_admin, *args, **kwargs)
    return decorated
