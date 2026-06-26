from flask import Blueprint, request, jsonify
from models import db
from models.customer import Customer
from utils.auth_utils import token_required

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/', methods=['GET'])
@token_required
def get_customers(current_admin):
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers]), 200

@customers_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_customer(current_admin, id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict()), 200

@customers_bp.route('/', methods=['POST'])
@token_required
def create_customer(current_admin):
    data = request.get_json()
    if Customer.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email already exists'}), 409
        
    new_customer = Customer(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        city=data.get('city'),
        budget=data.get('budget'),
        preferred_location=data.get('preferred_location'),
        interested_plot=data.get('interested_plot'),
        status=data.get('status', 'New'),
        priority=data.get('priority', 'Medium')
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(new_customer.to_dict()), 201

@customers_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(current_admin, id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    
    if 'email' in data and data['email'] != customer.email:
        if Customer.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 409
            
    for key, value in data.items():
        if hasattr(customer, key) and key != 'id':
            setattr(customer, key, value)
            
    db.session.commit()
    return jsonify(customer.to_dict()), 200

@customers_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_customer(current_admin, id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'}), 200
