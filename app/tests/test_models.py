import unittest
from app import app, db
from app.models import User, Subscription

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_user_model(self):
        user = User(username='testuser', email='testuser@test.com', password='testpassword')
        self.db.session.add(user)
        self.db.session.commit()

        queried_user = User.query.filter_by(username='testuser').first()
        self.assertEqual(queried_user.username, 'testuser')
        self.assertEqual(queried_user.email, 'testuser@test.com')

    def test_subscription_model(self):
        user = User(username='testuser', email='testuser@test.com', password='testpassword')
        self.db.session.add(user)
        self.db.session.commit()

        subscription = Subscription(user_id=user.id, plan='basic', status='active')
        self.db.session.add(subscription)
        self.db.session.commit()

        queried_subscription = Subscription.query.filter_by(user_id=user.id).first()
        self.assertEqual(queried_subscription.user_id, user.id)
        self.assertEqual(queried_subscription.plan, 'basic')
        self.assertEqual(queried_subscription.status, 'active')

if __name__ == '__main__':
    unittest.main()