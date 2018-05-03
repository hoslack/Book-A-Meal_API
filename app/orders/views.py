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

    def get(self):
        """This is a method for getting all orders from the database"""
        try:
            orders = Order.query.all()
            order_data = []

            #  make the data json serializable
            for order in orders:
                order_data.append({'id': order.id, 'customer_id': order.customer_id, 'meals': order.meals,
                                   'price': order.price})
            return jsonify({'data': order_data})
        except Exception as e:
            return jsonify({'Error occurred'.format(e)})


class OrderView(MethodView):
    """This is a class based view that handles the request made to a single order"""
    def __init__(self):
        super().__init__()

    def put(self, order_id):
        """This a method for handling editing of a single order"""
        if not order_id:
            return jsonify({'message': 'Please provide the order ID'})
        if not isinstance(order_id, int):
            return jsonify({'message': 'Invalid order ID'})
        json_data = request.get_json(force=True)
        meal1 = json_data.get('meal1')
        meal2 = json_data.get('meal2')
        price = json_data.get('price')
        # check if order exists
        order = Order.query.filter_by(id=order_id).first()
        try:
            if not order:
                return jsonify({'message': 'Order does not exist'})
            # check if order name exists
            if not meal1 and not meal2:
                return jsonify({'message': 'No meals provided'})
            # check if price exists
            if not price:
                return jsonify({'message': 'No price provided'})
            if not isinstance(price, int):
                return jsonify({'message': 'Invalid price'})
            if not isinstance(meal1, str):
                return jsonify({'message': 'Invalid meal name'})
            if not isinstance(meal2, str):
                return jsonify({'message': 'Invalid meal name'})
            order.meals = '{} and {}'.format(meal1, meal2)
            order.price = price
            order.save()
            return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'Error occurred {}'.format(e)})


#  define the meals class-based view
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

# add a url to be used to reach the view
orders_blueprint.add_url_rule('/orders/', view_func=orders_view, methods=['GET', 'POST'])
orders_blueprint.add_url_rule('/orders/<int:order_id>/', view_func=order_view, methods=['PUT'])
