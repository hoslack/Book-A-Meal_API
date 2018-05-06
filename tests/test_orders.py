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

    def test_cannot_order_without_token(self):
        res = self.client().post('/orders/', data=json.dumps({"customer_id": 4, "meals": "rice and beef", "price": 450}))
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_cannot_order_with_invalid_token(self):
        res = self.client().post('/orders/', headers=dict(Authorization="Bearer access_token"),
                                 data=json.dumps({"customer_id": 4, "meals": "rice and beef", "price": 450}))
        self.assertEqual(res.status_code, self.error.forbidden_status)

    def test_cannot_edit_order_without_token(self):
        res = self.client().put('/orders/1/', data=json.dumps({"meals": "rice and beef", "price": 450}))
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_edit_order_with_invalid_token(self):
        """Test if only user with valid token can edit order"""
        res = self.client().put('/orders/2/', headers=dict(Authorization="Bearer access_token"),
                                data=json.dumps({"name": "rice", "price": 300}))
        self.assertEqual(res.status_code, self.error.forbidden_status)

    def test_cannot_get_order_without_token(self):
        res = self.client().get('/orders/')
        self.assertEqual(res.status_code, self.error.unauthorized_status)

    def test_cannot_get_order_with_invalid_token(self):
        res = self.client().get('/orders/', headers=dict(Authorization="Bearer access_token"))
        self.assertEqual(res.status_code,  self.error.forbidden_status)


if __name__ == "__main__":
    unittest.main()
