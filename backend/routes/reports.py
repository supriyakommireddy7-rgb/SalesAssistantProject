from flask import Blueprint, jsonify
import csv
import os
from datetime import datetime
from models.customer import Customer
from models.report import Report
from models import db
from utils.auth_utils import token_required

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/csv', methods=['GET'])
@token_required
def generate_csv_report(current_admin):
    os.makedirs('generated_reports', exist_ok=True)
    
    filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = os.path.join('generated_reports', filename)
    
    customers = Customer.query.all()
    
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Status', 'Priority', 'Created At'])
        for c in customers:
            writer.writerow([c.id, c.name, c.email, c.phone, c.status, c.priority, c.created_at])
            
    new_report = Report(title=f"Customers Report {datetime.now().strftime('%Y-%m-%d')}", type="CSV", file_path=filepath)
    db.session.add(new_report)
    db.session.commit()
    
    return jsonify(new_report.to_dict()), 201

@reports_bp.route('/', methods=['GET'])
@token_required
def get_reports(current_admin):
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return jsonify([r.to_dict() for r in reports]), 200
