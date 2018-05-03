from flask_bcrypt import Bcrypt
from flask import current_app
from datetime import datetime, timedelta
import jwt
from app import db


class User(db.Model):
    """This is a model that defines every user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, admin=False):
        """Initialize a user """
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')
        self.admin = admin

    def is_password_valid(self, password):
        """Compare password with the harsh to check validity"""
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """Generate an access token required to log in user"""
        try:
            # create a payload to be used in generating token

            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            # generate a jwt encoded string
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_toke(token):
        """A method to decode access token from header"""
        try:
            # decode the token using the SECRET
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # if the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def save(self):
        """Save a user to the database"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Order(db.Model):
    """This is a model that holds all orders"""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    meals = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, customer_id, meals, price):
        """Initializing the order"""
        self.customer_id = customer_id
        self.meals = meals
        self.price = price

    def save(self):
        """Save an order to the database"""
        db.session.add(self)
        db.session.commit()


class MenuItem(db.Model):
    """This is a model to hold all the menu items"""

    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    meals = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer(256), nullable=False)

    def __init__(self, meals, price):
        """ Initialize menu item"""
        self.meals = meals
        self.price = price

    def save(self):
        """Save an item to the database"""
        db.session.add(self)
        db.session.commit()


class Meal(db.Model):
    """This is a model for all meals"""

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def save(self):
        """Save a meal to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """A method for deleting a meal from the database"""
        db.session.delete(self)
        db.session.commit()
