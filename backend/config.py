import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('JWT_SECRET', 'super-secret-key')
    # Using SQLite. On Vercel, use /tmp since the root filesystem is read-only.
    # We also check for DATABASE_URL for production (e.g. MySQL/Postgres).
    _db_path = '/tmp/app.db' if os.environ.get('VERCEL') else 'app.db'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{_db_path}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
