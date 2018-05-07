from flask.views import MethodView
from flask import request, jsonify
from app.models.models import Meal
from app.custom_http_respones.responses import Success, Error
from app.decorators.decorators import admin_only
from . import meals_blueprint


class MealsView(MethodView):
    def __init__(self):
        super().__init__()
        self.success = Success()
        self.error = Error()

    @admin_only
    def post(self, user_id):
        """This is a method to add a meal into the database"""
        json_data = request.get_json(force=True)
        name = json_data.get('name')
        price = json_data.get('price')
        # check if meal exists
        meal = Meal.query.filter_by(name=name).first()

        if not meal:
            try:
                # check if meal name exists exists
                if not name:
                    return self.error.bad_request('No name provided provided')
                # check if price exists
                if not price:
                    return self.error.bad_request('No email provided')
                if not isinstance(price, int):
                    return self.error.bad_request('Invalid price')
                if not isinstance(name, str):
                    return self.error.bad_request('Invalid price')
                meal = Meal(name=name, price=price)
                meal.save()
                return jsonify({"message": "Success", "id": meal.id})
            except Exception as e:
                return self.error.internal_server_error('Error occurred {}'.format(e))
        else:
            return self.error.causes_conflict('Meal exists')

    @admin_only
    def get(self, user_id):
        """This method gets all meals from the database"""
        try:
            meals = Meal.query.all()
            meal_data = []
            for meal in meals:
                meal_data.append({'id': meal.id, 'name': meal.name, 'price': meal.price})

            return self.success.complete_request('data: {}'.format(meal_data))
        except Exception as e:
            return self.error.internal_server_error('Error occurred'.format(e))


class MealView(MethodView):
    def __init__(self):
        super().__init__()
        self.success = Success()
        self.error = Error()

    @admin_only
    def put(self, user_id, meal_id):
        """This is a method to edit the details of a meal"""
        if not meal_id:
            return self.error.bad_request('Please provide the meal ID')
        if not isinstance(meal_id, int):
            return self.error.bad_request('Invalid meal ID')
        json_data = request.get_json(force=True)
        name = json_data.get('name')
        price = json_data.get('price')
        meal = Meal.query.filter_by(id=meal_id).first()  # check if meal exists
        try:
            if not meal:
                return self.error.causes_conflict('Meal does not exist')
            # check if meal name exists exists
            if not name:
                return self.error.bad_request('No name provided')
            # check if price exists
            if not price:
                return self.error.bad_request('No price provided')
            if not isinstance(price, int):
                return self.error.bad_request('Invalid price')
            if not isinstance(name, str):
                return self.error.bad_request('Invalid name')
            if meal.name == name:
                return self.error.causes_conflict('Cannot edit meal with same name')
            meal.name = name
            meal.price = price
            meal.save()
            return self.success.complete_request('Success')
        except Exception as e:
            return self.error.internal_server_error('Error occurred {}'.format(e))

    @admin_only
    def delete(self, user_id, meal_id):
        """This is a method to delete a single meal from the database"""
        if not meal_id:
            return self.error.bad_request('Please provide the meal ID')
        if not isinstance(meal_id, int):
            return self.error.bad_request('Invalid meal ID')
        meal = Meal.query.filter_by(id=meal_id).first()
        try:
            if not meal:
                return self.error.not_found('Meal does not exist')
            meal.delete()
            return self.success.complete_request('Success')
        except Exception as e:
            return self.error.internal_server_error('Error occurred {}'.format(e))


#  define the meals class-based view
meals_view = MealsView.as_view('meals_view')
meal_view = MealView.as_view('meal_view')


# add a url to be used to reach the view
meals_blueprint.add_url_rule('/meals/', view_func=meals_view, methods=['GET', 'POST'])
meals_blueprint.add_url_rule('/meals/<int:meal_id>/', view_func=meal_view, methods=['PUT', 'DELETE'])
