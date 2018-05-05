from flask import Blueprint


menu_blueprint = Blueprint('menu', __name__)

from . import views
