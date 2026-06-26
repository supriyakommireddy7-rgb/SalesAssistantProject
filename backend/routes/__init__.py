from .auth import auth_bp
from .customers import customers_bp
from .emails import emails_bp
from .conversations import conversations_bp
from .knowledge_base import kb_bp
from .dashboard import dashboard_bp
from .reports import reports_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(emails_bp, url_prefix='/api/emails')
    app.register_blueprint(conversations_bp, url_prefix='/api/conversations')
    app.register_blueprint(kb_bp, url_prefix='/api/knowledge_base')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
