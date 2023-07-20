import unittest
from flask import current_app
from app import create_app, db

class ErrorHandlingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response = self.client.get('/non-existant-route')
        self.assertEqual(response.status_code, 404)

    def test_500(self):
        response = self.client.get('/route-causing-500')
        self.assertEqual(response.status_code, 500)

    def test_403(self):
        response = self.client.get('/route-causing-403')
        self.assertEqual(response.status_code, 403)

    def test_401(self):
        response = self.client.get('/route-causing-401')
        self.assertEqual(response.status_code, 401)