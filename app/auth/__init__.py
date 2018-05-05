from flask import Blueprint

# Instantiating a blueprint for auth
auth_blueprint = Blueprint('auth', __name__)

from . import views
