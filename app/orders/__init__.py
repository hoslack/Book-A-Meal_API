from flask import Blueprint

# Instantiating a blueprint for orders
orders_blueprint = Blueprint('orders', __name__)

from . import views
