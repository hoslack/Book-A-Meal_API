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
            admin = User(email='admin@gmail.com', password='12345678', admin=True)
            admin.save()

    def test_add_meal_success(self):
        """Admin needs an admin token to add meal"""
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        res1 = self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                                  data=json.dumps({"name": "rice", "price": 300}))
        self.assertEqual(res1.status_code, self.success.ok_status)

    def test_add_meal_without_data(self):
        """Test if admin can add meal with not data"""
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        res1 = self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                                  data=json.dumps({}))
        self.assertEqual(res1.status_code, self.error.bad_request_status)

    def test_edit_meal_success(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        rv = self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                           data=json.dumps({"name": "tender goat", "price": 300}))
        rv_json = json.loads(rv.data)
        meal_id = rv_json['id']
        res = self.client().put('/meals/{}/'.format(meal_id), headers=dict(Authorization="Bearer " + token),
                                data=json.dumps({"name": "fish", "price": 300}))
        self.assertEqual(res.status_code, self.success.ok_status)

    def test_edit_meal_with_same_name(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        rv = self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                           data=json.dumps({"name": "tender goat", "price": 300}))
        rv_json = json.loads(rv.data)
        meal_id = rv_json['id']
        res = self.client().put('/meals/{}/'.format(meal_id), headers=dict(Authorization="Bearer " + token),
                                data=json.dumps({"name": "tender goat", "price": 300}))
        self.assertEqual(res.status_code, self.error.conflict_status)

    def test_edit_meal_with_no_data(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        rv = self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                                data=json.dumps({"name": "mushroom", "price": 300}))
        rv_json = json.loads(rv.data)
        meal_id = rv_json['id']
        res = self.client().put('/meals/{}/'.format(meal_id), headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, self.error.bad_request_status)

    def test_edit_non_existing_meal(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        res = self.client().put('/meals/-857/', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, self.error.not_found_status)

    def test_delete_meal_success(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        rv = self.client().post('/meals/', headers=dict(Authorization="Bearer " + token),
                                data=json.dumps({"name": "Cake", "price": 300}))
        rv_json = json.loads(rv.data)
        meal_id = rv_json['id']
        res = self.client().delete('/meals/{}/'.format(meal_id), headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, self.success.ok_status)

    def test_delete_non_existing_meal(self):
        res = self.client().post('/auth/login/', data=json.dumps({"email": "admin@gmail.com", "password": "12345678"}))
        json_data = json.loads(res.data)
        token = json_data['token']
        res = self.client().delete('/meals/-485/', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(res.status_code, self.error.not_found_status)

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
