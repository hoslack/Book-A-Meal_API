from flask.views import MethodView
from flask import jsonify
from flask import request
from app.models.models import Order
from decorators.decorators import token_required, admin_only
from . import orders_blueprint


class OrdersView(MethodView):
    """A class based view for handling orders requests"""
    def __init__(self):
        super().__init__()

    @token_required
    def post(self, user_id):
        """This method is for adding an order into the database"""
        json_data = request.get_json(force=True)
        customer_id = json_data.get('customer_id')
        price = json_data.get('price')
        meal_name = json_data.get('meals')

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
                if not isinstance(meal_name, str):
                    return jsonify({'message': 'Invalid meal name'})

                order = Order(customer_id=customer_id, meals=meal_name, price=price)
                order.save()
                return jsonify({'message': 'Success', 'id': order.id})
            except Exception as e:
                return jsonify({'message': 'Error occurred {}'.format(e)})
        else:
            return jsonify({'message': 'order exists'})

    @admin_only
    def get(self, user_id):
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

    @token_required
    def put(self, user_id, order_id):
        """This a method for handling editing of a single order"""
        if not order_id:
            return jsonify({'message': 'Please provide the order ID'})
        if not isinstance(order_id, int):
            return jsonify({'message': 'Invalid order ID'})
        json_data = request.get_json(force=True)
        meal_name = json_data.get('meals')
        price = json_data.get('price')
        # check if order exists
        order = Order.query.filter_by(id=order_id).first()
        try:
            if not order:
                return jsonify({'message': 'Order does not exist'})
            # check if order name exists
            if not meal_name:
                return jsonify({'message': 'No meals provided'})
            # check if price exists
            if not price:
                return jsonify({'message': 'No price provided'})
            if not isinstance(price, int):
                return jsonify({'message': 'Invalid price'})
            if not isinstance(meal_name, str):
                return jsonify({'message': 'Invalid meal name'})
            order.meals = meal_name
            order.price = price
            order.save()
            return jsonify({'message': 'Success'})
        except Exception as e:
            return jsonify({'message': 'Error occurred {}'.format(e)})


#  define the order class-based view
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

# add a url to be used to reach the view
orders_blueprint.add_url_rule('/orders/', view_func=orders_view, methods=['GET', 'POST'])
orders_blueprint.add_url_rule('/orders/<int:order_id>/', view_func=order_view, methods=['PUT'])
