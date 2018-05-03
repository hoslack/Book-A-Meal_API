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

        user = User.query.filter_by(email=json_data['email']).first() # check if user exists

        if not user:
            try:
                if not json_data['password']: # check if password exists
                    return jsonify({'message': 'No password provided'})
                if len(password) < 8:
                    return jsonify({'message': 'Password too short'})

                if not json_data['email']: # check if email exists
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


#  Define the view/resource
signup_view = SignUpView.as_view('signup_view')


# add a url to be used to reach the view
auth_blueprint.add_url_rule('/auth/signup/', view_func=signup_view, methods=['POST'])
