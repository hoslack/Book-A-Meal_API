import unittest
from flask import json
from app import create_app, db
from app.custom_http_respones.responses import Success, Error


class TestAuth(unittest.TestCase):
    """Test the authentication"""

    def setUp(self):
        """Setting up the variables for testing"""
        self.app = create_app(config_name='testing')
        self.app.testing = True
        self.client = self.app.test_client
        self.error = Error()
        self.success = Success()

        with self.app.app_context():
            # create all tables in the database
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration_success(self):
        """Test user registration works correctly"""
        res = self.client().post('/auth/signup/', data=json.dumps({"email": "hos@gmail.com", "password":"12345678"}))
        self.assertEqual(res.status_code, self.success.created_status)

    def test_signup_without_credentials(self):
        res = self.client().post('/auth/signup/', data=json.dumps({}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_signup_with_same_email(self):
        self.client().post('/auth/signup/', data=json.dumps({"email": "hos1@gmail.com", "password": "12345678"}))
        res = self.client().post('/auth/signup/', data=json.dumps({"email": "hos1@gmail.com", "password": "12345678"}))
        self.assertEqual(res.status_code, self.error.conflict_status)

    def test_signup_with_short_password(self):
        res = self.client().post('/auth/signup/', data=json.dumps({"email": "hos2@gmail.com", "password": "12345"}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

