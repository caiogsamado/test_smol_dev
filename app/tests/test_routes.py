import unittest
from app import app, db
from app.models import User, Subscription

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def test_login(self):
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'login_error', response.data)

    def test_register(self):
        response = self.app.post('/register', data=dict(
            username='testuser',
            email='testuser@test.com',
            password='testpassword',
            confirm='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'register_success', response.data)

    def test_create_subscription(self):
        self.app.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        response = self.app.post('/subscription', data=dict(
            name='Test Subscription',
            price='10.00',
            interval='month'
        ), follow_redirects=True)
        self.assertIn(b'subscription_success', response.data)

    def test_update_subscription(self):
        self.app.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.app.post('/subscription', data=dict(
            name='Test Subscription',
            price='10.00',
            interval='month'
        ), follow_redirects=True)
        response = self.app.post('/subscription/update', data=dict(
            name='Updated Subscription',
            price='15.00',
            interval='month'
        ), follow_redirects=True)
        self.assertIn(b'subscription_success', response.data)

if __name__ == '__main__':
    unittest.main()