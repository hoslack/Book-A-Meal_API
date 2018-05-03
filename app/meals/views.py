from flask.views import MethodView
from flask import jsonify
from flask import request
from app.models.models import Meal
from . import meals_blueprint


class MealsView(MethodView):
    def __init__(self):
        super().__init__()

    def post(self):
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
                    return jsonify({'message': 'No name provided provided'})
                # check if price exists
                if not price:
                    return jsonify({'message': 'No email provided'})
                if not isinstance(price, int):
                    return jsonify({'message': 'Invalid price'})
                if not isinstance(name, str):
                    return jsonify({'message': 'Invalid price'})
                meal = Meal(name=name, price=price)
                meal.save()
                return jsonify({'message': 'Success', 'id': meal.id})
            except Exception as e:
                return jsonify({'message': 'Error occurred {}'.format(e)})
        else:
            return jsonify({'message': 'Meal exists'})

    def get(self):
        """This method gets all meals from the database"""
        try:
            meals = Meal.query.all()
            meal_data = []
            for meal in meals:
                meal_data.append({'id': meal.id, 'name': meal.name, 'price': meal.price})

            return jsonify({'data': meal_data})
        except Exception as e:
            return jsonify({'Error occurred'.format(e)})


class MealView(MethodView):
    def __init__(self):
        super().__init__()

    def put(self, meal_id):
        """This is a method to edit the details of a meal"""
        if not meal_id:
            return jsonify({'message': 'Please provide the meal ID'})
        if not isinstance(meal_id, int):
            return jsonify({'message': 'Invalid meal ID'})
        json_data = request.get_json(force=True)
        name = json_data.get('name')
        price = json_data.get('price')
        meal = Meal.query.filter_by(id=meal_id).first()  # check if meal exists
        try:
            if not meal:
                return jsonify({'message': 'Meal does not exist'})
            # check if meal name exists exists
            if not name:
                return jsonify({'message': 'No name provided'})
            # check if price exists
            if not price:
                return jsonify({'message': 'No price provided'})
            if not isinstance(price, int):
                return jsonify({'message': 'Invalid price'})
            if not isinstance(name, str):
                return jsonify({'message': 'Invalid name'})
            meal.name = name
            meal.price = price
            meal.save()
            return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'Error occurred {}'.format(e)})

    def delete(self, meal_id):
        """This is a method to delete a single meal from the database"""
        if not meal_id:
            return jsonify({'message': 'Please provide the meal ID'})
        if not isinstance(meal_id, int):
            return jsonify({'message': 'Invalid meal ID'})
        meal = Meal.query.filter_by(id=meal_id).first()
        try:
            if not meal:
                return jsonify({'message': 'Meal does not exist'})
            meal.delete()
            return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'Error occurred {}'.format(e)})


#  define the meals class-based view
meals_view = MealsView.as_view('meals_view')
meal_view = MealView.as_view('meal_view')


# add a url to be used to reach the view
meals_blueprint.add_url_rule('/meals/', view_func=meals_view, methods=['GET', 'POST'])
meals_blueprint.add_url_rule('/meals/<int:meal_id>/', view_func=meal_view, methods=['PUT', 'DELETE'])
