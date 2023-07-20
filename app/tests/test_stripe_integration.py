import unittest
from app import app, db
from app.models import User, Subscription
from app.stripe_integration import create_subscription, update_subscription

class TestStripeIntegration(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db

        self.test_user = User(username='testuser', email='testuser@test.com')
        self.test_subscription = Subscription(name='Test Subscription', price=10.00, user_id=self.test_user.id)

        self.db.session.add(self.test_user)
        self.db.session.add(self.test_subscription)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_create_subscription(self):
        response = create_subscription(self.test_user.id, self.test_subscription.id)
        self.assertEqual(response.status, 'active')

    def test_update_subscription(self):
        response = update_subscription(self.test_user.id, self.test_subscription.id)
        self.assertEqual(response.status, 'active')

if __name__ == "__main__":
    unittest.main()