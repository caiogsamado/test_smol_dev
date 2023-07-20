import unittest
from app import app, db
from app.forms import LoginForm, RegisterForm, SubscriptionForm
from app.models import User, Subscription

class TestForms(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_form(self):
        form = LoginForm(email='test@test.com', password='password')
        self.assertTrue(form.validate())

    def test_register_form(self):
        form = RegisterForm(email='test@test.com', password='password', confirm='password')
        self.assertTrue(form.validate())

    def test_create_subscription_form(self):
        form = SubscriptionForm(doctor_id=1, patient_id=1, plan='basic')
        self.assertTrue(form.validate())

    def test_update_subscription_form(self):
        form = SubscriptionForm(doctor_id=1, patient_id=1, plan='premium')
        self.assertTrue(form.validate())

if __name__ == "__main__":
    unittest.main()