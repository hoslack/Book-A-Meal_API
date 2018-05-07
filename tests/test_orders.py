import os
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
        os.environ["SECRET"] = "989d554b-1598-4b77-bf22-0941953cd955"

        with self.app.app_context():
            # create all tables in the database
            db.session.close()
            db.drop_all()
            db.create_all()
            user = User(email='hos@gmail.com', password='12345678')
            admin = User(email='admin@gmail.com', password='12345678', admin=True)
            user.save()
            admin.save()

    def test_get_orders_success(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        res1 = self.client().get('/orders/', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res1.status_code, self.success.ok_status)

    def test_add_orders_success(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                           data=json.dumps({"name": "rice", "price": 300}))
        self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                           data=json.dumps({"name": "beef", "price": 300}))
        res1 = self.client().post('/orders/', headers=dict(Authorization="Bearer " + token),
                                  data=json.dumps({"meal1": "rice", "meal2": "beef", "price": 300}))
        self.assertEqual(res1.status_code, self.success.created_status)

    def test_add_orders_not_in_db(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "hos@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        res1 = self.client().post('/orders/', headers=dict(Authorization="Bearer " + token),
                                  data=json.dumps({"meal1": "anymeal", "meal2": "random", "price": 300}))
        self.assertEqual(res1.status_code, self.error.not_found_status)

    def test_edit_order_success(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                           data=json.dumps({"name": "rice", "price": 300}))
        self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                           data=json.dumps({"name": "beef", "price": 300}))
        self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                           data=json.dumps({"name": "pilau", "price": 300}))
        self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                           data=json.dumps({"name": "soup", "price": 300}))
        res1 = self.client().post('/orders/', headers=dict(Authorization="Bearer " + token),
                                  data=json.dumps({"meal1": "rice", "meal2": "beef", "price": 300}))
        res1_json = json.loads(res1.data)
        order_id = res1_json['id']
        res1 = self.client().put('/orders/{}/'.format(order_id), headers=dict(Authorization="Bearer " + token),
                                 data=json.dumps({"meal1": "pilau", "meal2": "soup", "price": 300}))
        self.assertEqual(res1.status_code, self.success.created_status)


    def test_add_orders_without_data(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "hos@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        res1 = self.client().post('/orders/', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res1.status_code, self.error.bad_request_status)

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
