from flask import Blueprint

# Instantiating a blueprint for meals
meals_blueprint = Blueprint('meals', __name__)

from . import views
