from app import db, create_app
from flask_bcrypt import Bcrypt


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
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.admin = admin

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
    meals = db.Column(db.String, nullable=False)
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
    meals = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

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
    name = db.Column(db.String, nullable=False)
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
