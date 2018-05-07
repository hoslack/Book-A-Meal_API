import unittest
import os
from flask import jsonify, json
from app import create_app, db
from app.models.models import User
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
        os.environ["SECRET"] = "989d554b-1598-4b77-bf22-0941953cd955"

        with self.app.app_context():
            # create all tables in the database
            db.session.close()
            db.drop_all()
            db.create_all()
            admin = User(email='admin@gmail.com', password='12345678', admin=True)
            admin.save()

    def test_sign_in_another_admin(self):
        """Admin needs an admin token to register another user"""
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data.decode())
        token = json_data['token']
        res1 = self.client().post('/auth/signup/admin/', headers=dict(Authorization="Bearer " + token),
                                  data=json.dumps({"email": "admin2@gmail.com", "password": "12345678"}))
        self.assertEqual(res1.status_code, self.success.created_status)

    def test_sign_in_another_admin_no_data(self):
        """Admin needs an admin token to register another user"""
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data.decode())
        token = json_data['token']
        res1 = self.client().post('/auth/signup/admin/', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res1.status_code, self.error.bad_request_status)

    def test_signup_success(self):
        """Test user registration works correctly"""
        res = self.client().post('/auth/signup/', data=json.dumps({"email": "hos@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        self.assertEqual(json_data['message'], 'User created successfully')
        self.assertEqual(res.status_code, self.success.created_status)

    def test_admin_login(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        self.assertEqual(res.status_code, self.success.ok_status)

    def test_registration_admin_with_no_token(self):
        """Test user registration of admin requires token"""
        res = self.client().post('/auth/signup/admin/', data=json.dumps({"email": "hos@gmail.com", "password":"12345678"}))
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_signup_without_credentials(self):
        res = self.client().post('/auth/signup/', data=json.dumps({}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_signup_without_email(self):
        """Test if user can sign in with no email"""
        res = self.client().post('/auth/signup/', data=json.dumps({"email": "hos@gmail.com"}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_signup_without_password(self):
        """Test if user can sign in with no password"""
        res = self.client().post('/auth/signup/', data=json.dumps({"password": "12345678"}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_signup_with_same_email(self):
        self.client().post('/auth/signup/', data=json.dumps({"email": "hos1@gmail.com", "password": "12345678"}))
        res = self.client().post('/auth/signup/', data=json.dumps({"email": "hos1@gmail.com", "password": "12345678"}))
        self.assertEqual(res.status_code, self.error.conflict_status)

    def test_signup_with_short_password(self):
        res = self.client().post('/auth/signup/', data=json.dumps({"email": "hos2@gmail.com", "password": "12345"}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_signup_with_invalid_email(self):
        res = self.client().post('/auth/signup/', data=json.dumps({"email": "hos2gmail.com", "password": "12345"}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_successful_login(self):
        self.client().post('/auth/signup/', data=json.dumps({"email": "hos@gmail.com", "password": "12345678"}))
        res = self.client().post('/auth/login/', data=json.dumps({"email": "hos@gmail.com", "password": "12345678"}))
        self.assertEqual(res.status_code, self.success.ok_status)

    def test_login_non_existent_user(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "randomuserthatdoesnotexist@gmail.com",
                                                                  "password": "12345678"}))
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_login_with_no_credentials(self):
        res = self.client().post('/auth/login/', data=json.dumps({}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_login_with_no_email(self):
        res = self.client().post('/auth/signup/', data=json.dumps({"password": "12345678"}))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_admin_login_with_invalid_email(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admingmail.com", "password": "12345678"}))
        json_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(json_data['error'], 'Invalid email')
        self.assertEqual(res.status_code, 400)

    def test_admin_login_with_invalid_password(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "123456"}))
        json_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(json_data['error'], 'Password too short')
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
