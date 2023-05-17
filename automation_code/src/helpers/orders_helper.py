import pdb

from automation_code.src.utilities.requests_utility import RequestsUtility
from automation_code.src.dao.orders_dao import OrdersDAO
import os
import json

class OrdersHelper(object):

    def __init__(self):
        self.cur_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.requests_utility = RequestsUtility()

    def retrieve_order(self, order_id):
        order_api_res = self.requests_utility.get(f"orders/{order_id}", expected_status_code=200)
        return order_api_res

    # TODO do the order template fetching via a method
    def create_order(self, additional_args=None):

        payload_template = os.path.join(self.cur_file_dir, '..', 'data', 'create_order_payload.json')
        # In the data (create_order_payload.json) verify that the product id used exists.
        # "line_items": [{"product_id": 12,"quantity": 1}
        # If the product does not exist you will get 'completed' status for order when created.
        # The default should be 'processing' if the product is valid.

        with open(payload_template) as f:
            payload = json.load(f)

        # If user adds more info to payload, then update it
        if additional_args:
            assert isinstance(additional_args, dict), "Parameter 'additional_args' must be a dictionary"
            payload.update(additional_args)

        res_api = self.requests_utility.post('orders', payload=payload, expected_status_code=201)
        return res_api

    def create_order_payload(self, additional_args=None):
        payload_template = os.path.join(self.cur_file_dir, '..', 'data', 'create_order_payload.json')
        with open(payload_template) as f:
            payload = json.load(f)
        # If user adds more info to payload, then update it
        if additional_args:
            assert isinstance(additional_args, dict), "Parameter 'additional_args' must be a dictionary"
            payload.update(additional_args)
        return payload

    def update_order(self, order_id, **kwargs):
        payload = dict()
        payload.update(kwargs)
        update_order_json = self.requests_utility.put(f'orders/{order_id}', payload=payload, expected_status_code=200)
        return update_order_json


    @staticmethod
    def verify_order_is_created(order_json, exp_cust_id, exp_products):

        orders_dao = OrdersDAO()

        # Verify in API response
        assert order_json, f"Create order response is empty."
        assert order_json['customer_id'] == exp_cust_id, f"Create order with given customer id... \
                                Expected customer_id: {exp_cust_id} Actual:  '{order_json['customer_id']}'"

        assert len(order_json['line_items']) == len(exp_products), f"Expected {len(exp_products)} item/s in order " \
                                                                   f"Actual: '{len(order_json['line_items'])}'" \
                                                                   f"Order id: {order_json['id']}."
        # Verify in DB
        order_id = order_json['id']
        item_info = orders_dao.get_order_table_data("woocommerce_order_items ", "order_id", order_id)
        assert item_info, f"Create order, line item not found in DB. Order id: {order_id}"

        db_items = [i for i in item_info if i['order_item_type'] == 'line_item']
        assert len(db_items) == 1, f"Expected 1 line item but found {len(db_items)}. Order id: {order_id}"

        # Get list of product ids in the response
        api_product_ids = [i['product_id'] for i in order_json['line_items']]

        for product in exp_products:
            assert product[
                       'product_id'] in api_product_ids, f"Create order does not have at least 1 expected product in DB." \
                                                         f"Product id: {product['product_id']}. Order id: {order_id}"