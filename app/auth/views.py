from flask.views import MethodView
from flask import jsonify
from flask import request
import re
from app.models.models import User
from . import auth_blueprint


class SignUpView(MethodView):

    def __init__(self):
        super().__init__()

    def post(self):
        """This method handles the registration route"""

        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        # check if user exists
        user = User.query.filter_by(email=json_data['email']).first()

        if not user:
            try:
                # check if password exists
                if not json_data['password']:
                    return jsonify({'message': 'No password provided'})
                if len(password) < 8:
                    return jsonify({'message': 'Password too short'})
                # check if email exists
                if not json_data['email']:
                    return jsonify({'message': 'No email provided'})
                regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                if not re.match(regex, email):
                    return jsonify({'message': 'Invali email'})

                user = User(email=email, password=password)
                user.save()
                return jsonify({'message': 'Success'})
            except Exception as e:
                return jsonify({'message': 'Error occurred {}'.format(e)})
        else:
            return jsonify({'message': 'User exists'})


class LoginView(MethodView):
    """This is a view for handling user login and assigning of tokens"""
    def __init__(self):
        super().__init__()

    def post(self):
        """A method for handling the log in request endpoint"""
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        try:
            # check if password exists
            if not email:
                return jsonify({'message': 'No password provided'})
            if len(password) < 8:
                return jsonify({'message': 'Password too short'})
            # check if email exists
            if not email:
                return jsonify({'message': 'No email provided'})
            regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not re.match(regex, email):
                return jsonify({'message': 'Invalid email'})
            # Get the user object
            user = User.query.filter_by(email=email).first()
            # Authenticate the user
            if user and user.is_password_valid(password):
                # Generate the access token to be used in header
                access_token = user.generate_token(user.id)
                if access_token:
                    return jsonify({
                        'message': 'Log in successful',
                        'access_token': access_token.decode()
                    })
            else:
                return jsonify({'message': 'Invalid email or password'})
        except Exception as e:
            return str(e)


#  Define the views/resources
signup_view = SignUpView.as_view('signup_view')
login_view = LoginView.as_view('login_view')


# add a url to be used to reach the view
auth_blueprint.add_url_rule('/auth/signup/', view_func=signup_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login/', view_func=login_view, methods=['POST'])
