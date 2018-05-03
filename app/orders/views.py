from flask.views import MethodView
from flask import jsonify
from flask import request
from app.models.models import Order
from . import orders_blueprint


class OrdersView(MethodView):
    """A class based view for handling orders requests"""
    def __init__(self):
        super().__init__()

    def post(self):
        """This method is for adding an order into the database"""
        json_data = request.get_json(force=True)
        customer_id = json_data.get('customer_id')
        meal1 = json_data.get('meal1')
        meal2 = json_data.get('meal2')
        price = json_data.get('price')
        meal_name = '{} and {}'.format(meal1, meal2)

        # check if meals exist
        meal = Order.query.filter_by(meals=meal_name).first()

        if not meal:
            try:
                # check if meal name exists exists
                if not customer_id:
                    return jsonify({'message': 'No customer id provided'})
                if not isinstance(customer_id, int):
                    return jsonify({'message': 'Invalid customer id'})
                # check if price exists
                if not price:
                    return jsonify({'message': 'No price provided'})
                if not isinstance(price, int):
                    return jsonify({'message': 'Invalid price'})
                if not isinstance(meal1, str):
                    return jsonify({'message': 'Invalid meal name'})
                if not isinstance(meal2, str):
                    return jsonify({'message': 'Invalid meal name'})

                order = Order(customer_id=customer_id, meals=meal_name, price=price)
                order.save()
                return jsonify({'message': 'Success', 'id': order.id})
            except Exception as e:
                return jsonify({'message': 'Error occurred {}'.format(e)})
        else:
            return jsonify({'message': 'order exists'})


#  define the meals class-based view
orders_view = OrdersView.as_view('orders_view')
# order_view = OrderView.as_view('order_view')

# add a url to be used to reach the view
orders_blueprint.add_url_rule('/orders/', view_func=orders_view, methods=['GET', 'POST'])
# orders_blueprint.add_url_rule('/orders/<int:order_id>/', view_func=order_view, methods=['PUT'])
