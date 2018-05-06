import unittest
from flask import json
from app import create_app, db
from app.custom_http_respones.responses import Success, Error
from app.models.models import User


class TestAuth(unittest.TestCase):
    """Test the meal routes and db"""

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
            admin = User(email='admin@gmail.com', password='12345678', admin=True)
            admin.save()

    def test_admin_login(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": '12345678'}))
        self.assertEqual(res.status_code, self.success.ok_status)

    def test_add_meal_without_token(self):
        """Test if only logged user can add meal"""
        res = self.client().post('/meals/', data=json.dumps({"name": "rice", "price": 300}))
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_add_meal_with_invalid_token(self):
        """Test if only admin with valid token can add meal"""
        res = self.client().post('/meals/', headers=dict(Authorization="Bearer access_token"),
                                 data=json.dumps({"name": "rice", "price": 300}))
        self.assertEqual(res.status_code, self.error.forbidden_status)

    def test_get_meals_without_token(self):
        """Test if only logged user can get meals"""
        res = self.client().get('/meals/')
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_get_meals_with_invalid_token(self):
        """Test if only admin with valid token can get meals"""
        res = self.client().get('/meals/', headers=dict(Authorization="Bearer access_token"))
        self.assertEqual(res.status_code, self.error.forbidden_status)

    def test_edit_meal_without_token(self):
        """Test if only logged user can add meal"""
        res = self.client().put('/meals/2/', data=json.dumps({"name": "rice", "price": 300}))
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_edit_meal_with_invalid_token(self):
        """Test if only admin with valid token can edit meal"""
        res = self.client().put('/meals/2/', headers=dict(Authorization="Bearer access_token"),
                                data=json.dumps({"name": "rice", "price": 300}))
        self.assertEqual(res.status_code, self.error.forbidden_status)


if __name__ == "__main__":
    unittest.main()
