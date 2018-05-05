from flask.views import MethodView
from flask import request
from app.models.models import Order
from app.helpers.helpers import Helpers
from app.decorators.decorators import token_required, admin_only
from app.custom_http_respones.responses import Success, Error
from . import orders_blueprint


class OrdersView(MethodView):
    """A class based view for handling orders requests"""
    def __init__(self):
        super().__init__()
        self.helpers = Helpers()
        self.success = Success()
        self.error = Error()

    @token_required
    def post(self, user_id):
        """This method is for adding an order into the database"""
        json_data = request.get_json(force=True)
        price = json_data.get('price')
        meal1 = json_data.get('meal1')
        meal2 = json_data.get('meal2')
        if not self.helpers.meal_in_db(meal1) or not self.helpers.meal_in_db(meal2):
            return self.error.not_found('One or both meals not in db')
        meal_name = '{} and {}'.format(meal1, meal2)
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        customer_id = self.helpers.current_user(access_token)

        # check if meals exist
        meal = Order.query.filter_by(meals=meal_name).first()

        if not meal:
            try:
                # check if meal name exists exists
                if not customer_id:
                    return self.error.bad_request('No customer id provided')
                if not isinstance(customer_id, int):
                    return self.error.bad_request('Invalid customer id')
                # check if price exists
                if not price:
                    return self.error.bad_request('No price provided')
                if not isinstance(price, int):
                    return self.error.bad_request('Invalid price')
                if not isinstance(meal_name, str):
                    return self.error.bad_request('Invalid meal name')

                order = Order(customer_id=customer_id, meals=meal_name, price=price)
                order.save()
                return self.success.create_resource('Success, id:'.format(order.id))
            except Exception as e:
                return self.error.internal_server_error('Error occurred {}'.format(e))
        else:
            return self.error.causes_conflict('Order exists')

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
            return self.success.complete_request({'data': order_data})
        except Exception as e:
            return self.error.internal_server_error('Error occurred'.format(e))


class OrderView(MethodView):
    """This is a class based view that handles the request made to a single order"""
    def __init__(self):
        super().__init__()
        self.helpers = Helpers()
        self.success = Success()
        self.error = Error()

    @token_required
    def put(self, user_id, order_id):
        """This a method for handling editing of a single order"""
        if not order_id:
            return self.error.bad_request('Please provide the order ID')
        if not isinstance(order_id, int):
            return self.error.bad_request('Invalid order ID')
        json_data = request.get_json(force=True)
        price = json_data.get('price')
        meal1 = json_data.get('meal1')
        meal2 = json_data.get('meal2')
        if not self.helpers.meal_in_db(meal1) or not self.helpers.meal_in_db(meal2):
            return self.error.causes_conflict('One or both meals not in db')
        meal_name = '{} and {}'.format(meal1, meal2)

        # check if order exists
        order = Order.query.filter_by(id=order_id).first()
        try:
            if not order:
                return self.error.bad_request('Order does not exist')
            # check if order name exists
            if not meal_name:
                return self.error.bad_request('No meals provided')
            # check if price exists
            if not price:
                return self.error.bad_request('No price provided')
            if not isinstance(price, int):
                return self.error.bad_request('Invalid price')
            if not isinstance(meal_name, str):
                return self.error.bad_request('Invalid meal name')
            if order.meals == meal_name:
                return self.error.causes_conflict('Cannot edit to the same meal')
            order.meals = meal_name
            order.price = price
            order.save()
            return self.success.create_resource('Success')
        except Exception as e:
            return self.error.internal_server_error('Error occurred {}'.format(e))


#  define the order class-based view
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

# add a url to be used to reach the view
orders_blueprint.add_url_rule('/orders/', view_func=orders_view, methods=['GET', 'POST'])
orders_blueprint.add_url_rule('/orders/<int:order_id>/', view_func=order_view, methods=['PUT'])
