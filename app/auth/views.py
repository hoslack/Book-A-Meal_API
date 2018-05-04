from flask.views import MethodView
from flask import request
from app.models.models import User
from app.custom_http_respones.responses import Success, Error
from app.helpers.helpers import Helpers
from app.decorators.decorators import admin_only
from . import auth_blueprint


class SignUpView(MethodView):

    def __init__(self):
        super().__init__()
        self.helpers = Helpers()
        self.success = Success()
        self.error = Error()

    def post(self):
        """This method handles the registration route"""

        json_data = request.get_json(force=True)
        email = json_data.get('email')
        password = json_data.get('password')
        # check if user exists
        user = User.query.filter_by(email=json_data.get('email')).first()

        if not user:
            try:
                # check if password exists
                if not json_data.get('password'):
                    return self.error.bad_request('No password provided')
                if len(password) < 8:
                    return self.error.bad_request('Password too short')
                # check if email exists
                if not json_data.get('email'):
                    return self.error.bad_request('No email provided')
                if not self.helpers.email_valid(email):
                    return self.error.bad_request('Invalid email')

                user = User(email=email, password=password)
                user.save()
                return self.success.create_resource('User created successfully')
            except Exception as e:
                return self.error.internal_server_error('Error occurred {}'.format(e))
        else:
            return self.error.causes_conflict('User already exists')


class AdminSignUpView(MethodView):

    def __init__(self):
        super().__init__()
        self.helpers = Helpers()
        self.success = Success()
        self.error = Error()

    @admin_only
    def post(self, user_id):
        """This method handles the registration route for an admin"""

        json_data = request.get_json(force=True)
        email = json_data.get('email')
        password = json_data.get('password')
        # check if user exists
        user = User.query.filter_by(email=json_data.get('email')).first()

        if not user:
            try:
                # check if password exists
                if not json_data.get('password'):
                    return self.error.bad_request('No password provided')
                if len(password) < 8:
                    return self.error.bad_request('Password too short')
                # check if email exists
                if not json_data.get('email'):
                    return self.error.bad_request('No email provided')
                if not self.helpers.email_valid(email):
                    return self.error.bad_request('Invalid email')

                user = User(email=email, password=password, admin=True)
                user.save()
                return self.success.create_resource('User created successfully')
            except Exception as e:
                return self.error.internal_server_error('Error occurred {}'.format(e))
        else:
            return self.error.causes_conflict('User already exists')


class LoginView(MethodView):
    """This is a view for handling user login and assigning of tokens"""
    def __init__(self):
        super().__init__()
        self.helpers = Helpers()
        self.success = Success()
        self.error = Error()

    def post(self):
        """A method for handling the log in request endpoint"""
        json_data = request.get_json(force=True)
        email = json_data.get('email')
        password = json_data.get('password')
        try:
            # check if password exists
            if not email:
                return self.error.bad_request('No password provided')
            if len(password) < 8:
                return self.error.bad_request('Password too short')
            # check if email exists
            if not email:
                return self.error.bad_request('No email provided')
            if not self.helpers.email_valid(email):
                return self.error.bad_request('Invalid email')
            # Get the user object
            user = User.query.filter_by(email=email).first()
            # Authenticate the user
            if user and user.is_password_valid(password):
                # Generate the access token to be used in header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = 'Log in successful: id:{}'.format(access_token.decode())
                    return self.success.complete_request(response)
            else:
                return self.error.unauthorized('Invalid email or password')
        except Exception as e:
            return str(e)


#  Define the views/resources
signup_view = SignUpView.as_view('signup_view')
login_view = LoginView.as_view('login_view')
admin_signup_view = AdminSignUpView.as_view('admin_signup_view')

# add a url to be used to reach the view
auth_blueprint.add_url_rule('/auth/signup/', view_func=signup_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login/', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/signup/admin/', view_func=admin_signup_view, methods=['POST'])

