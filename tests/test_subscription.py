import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Subscription

class SubscriptionModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_subscription_model(self):
        u = User(email='doctor@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        s = Subscription(name='Basic', price=100, user_id=u.id)
        db.session.add(s)
        db.session.commit()
        self.assertTrue(s in u.subscriptions)
        self.assertTrue(s.user_id == u.id)

    def test_subscription_url(self):
        u = User(email='doctor@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        s = Subscription(name='Basic', price=100, user_id=u.id)
        db.session.add(s)
        db.session.commit()
        with self.app.test_request_context():
            url = url_for('main.subscription', id=s.id)
            self.assertTrue('/subscription/' in url)

if __name__ == '__main__':
    unittest.main()