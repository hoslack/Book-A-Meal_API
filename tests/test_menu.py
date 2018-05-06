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
            user = User(email='hos@gmail.com', password='12345678')
            user.save()

    def test_cannot_create_menu_without_token(self):
        res = self.client().post('/menu/', data=json.dumps({"meal1": "rice", "meal2": "beef", "price": 450}))
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_cannot_create_menu_with_invalid_token(self):
        res = self.client().post('/menu/', headers=dict(Authorization="Bearer access_token"),
                                 data=json.dumps({"meal1": "rice", "meal2": "beef", "price": 450}))
        self.assertEqual(res.status_code, self.error.forbidden_status)

    def test_cannot_get_menu_without_token(self):
        res = self.client().get('/menu/')
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_get_menu_with_invalid_token(self):
        res = self.client().get('/menu/', headers=dict(Authorization="Bearer access_token"))
        self.assertEqual(res.status_code, self.error.forbidden_status)


if __name__ == "__main__":
    unittest.main()
