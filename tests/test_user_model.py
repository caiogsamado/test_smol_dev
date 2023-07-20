import unittest
from app.models import User, db
from flask import current_app

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = current_app._get_current_object()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_role(self):
        u = User(email='doctor@example.com', password='cat')
        self.assertTrue(u.role.name == 'User')

    def test_admin_role(self):
        u = User(email='admin@example.com', password='cat')
        self.assertTrue(u.role.name == 'Administrator')

if __name__ == '__main__':
    unittest.main()