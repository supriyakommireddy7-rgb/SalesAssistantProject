import unittest
from backend.app import create_app
from backend.models import db
from backend.models.admin import Admin
import bcrypt

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            hashed_pw = bcrypt.hashpw('testpass'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = Admin(username='testadmin', password_hash=hashed_pw)
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_success(self):
        response = self.client.post('/api/auth/login', json={
            'username': 'testadmin',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_login_failure(self):
        response = self.client.post('/api/auth/login', json={
            'username': 'testadmin',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
