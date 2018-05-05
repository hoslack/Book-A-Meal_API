import re
from app.models.models import User, Meal, Order


class Helpers(object):
    """This class contains methods which are routinely used to avoid repetition"""

    def __init__(self):
        self.regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def email_valid(self, email):
        """A helper for validating emails"""
        if re.match(self.regex, email):
            return True
        else:
            return False

    def current_user(self, token):
        user_id = User.decode_token(token)
        return user_id

    def meal_in_db(self, meal):
        checked_meal = Meal.query.filter_by(name=meal).first()
        if checked_meal:
            return True
        else:
            return False
