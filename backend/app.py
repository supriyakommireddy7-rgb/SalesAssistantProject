from flask import Flask
from flask_cors import CORS
from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    # Import routes here to avoid circular imports
    from routes import register_routes
    register_routes(app)
    
    with app.app_context():
        db.create_all()
        
        # Auto-seed admin user if it doesn't exist (for Vercel / empty SQLite DBs)
        from models.admin import Admin
        import bcrypt
        if not Admin.query.filter_by(username='admin').first():
            hashed_pw = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            new_admin = Admin(username='admin', password_hash=hashed_pw.decode('utf-8'))
            db.session.add(new_admin)
            db.session.commit()
            print("Auto-seeded default admin user (admin:admin123)")
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
