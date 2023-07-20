import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Payment
from app.stripe_keys import stripe_public_key, stripe_secret_key
import stripe

class PaymentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_payment(self):
        # create a user
        u = User(email='john@example.com', password='cat')
        db.session.add(u)
        db.session.commit()

        # login the user
        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)

        # create a payment
        stripe.api_key = stripe_secret_key
        charge = stripe.Charge.create(
            amount=2000,
            currency='usd',
            description='Subscription for john@example.com',
            source='tok_visa'
        )

        payment = Payment(user_id=u.id, amount=2000, stripe_charge_id=charge.id)
        db.session.add(payment)
        db.session.commit()

        # check if the payment is recorded
        p = Payment.query.filter_by(user_id=u.id).first()
        self.assertIsNotNone(p)
        self.assertEqual(p.amount, 2000)
        self.assertEqual(p.stripe_charge_id, charge.id)