import unittest
from app import create_app
from app.models.models import User, Meal, MenuItem, Order


class TestAuth(unittest.TestCase):
    """Test the authentication"""

    def setUp(self):
        """Setting up the variables for testing"""
        self.app = create_app(config_name='testing')
        self.app.testing = True
        self.user_obj = User(email='hos@gmail.com', password='12345678')
        self.meal_obj = Meal(name='rice', price=120)
        self.menu_obj = MenuItem(meals='rice and beef', price=300)
        self.order_obj = Order(customer_id=4, meals='rice and beef', price=400)

    def test_user_is_obj(self):
        self.assertIsInstance(self.user_obj, User)

    def test_meal_is_obj(self):
        self.assertIsInstance(self.meal_obj, Meal)

    def test_menu_is_obj(self):
        self.assertIsInstance(self.menu_obj, MenuItem)

    def test_order_is_obj(self):
        self.assertIsInstance(self.order_obj, Order)

    def test_user_has_attributes(self):
        self.assertEqual(hasattr(User, 'save'), True)
        self.assertEqual(hasattr(User, 'email'), True)
        self.assertEqual(hasattr(User, 'password'), True)
        self.assertEqual(hasattr(User, 'admin'), True)
        self.assertEqual(hasattr(User, 'generate_token'), True)
        self.assertEqual(hasattr(User, 'is_password_valid'), True)






if __name__ == "__main__":
    unittest.main()
