from flask import Flask
from instance.config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])  # Configure app according to the environment
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    Migrate(app, db)
    from .auth import auth_blueprint  # include the views, in form of blueprints
    from .meals import meals_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(meals_blueprint)
    return app
