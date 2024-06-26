import pdb

import pytest
import random
from automation_code.src.dao.products_dao import ProductsDAO
from automation_code.src.dao.orders_dao import OrdersDAO
from automation_code.src.helpers.orders_helper import OrdersHelper
from automation_code.src.helpers.customers_helper import CustomerHelper
from automation_code.src.helpers.products_helper import ProductsHelper
from automation_code.src.utilities import generic_utility
from automation_code.src.utilities.requests_utility import RequestsUtility
from automation_code.src.utilities.generic_utility import generate_random_string

pytestmark = pytest.mark.order


@pytest.mark.smoke
def test_create_paid_order_guest_user(my_orders_smoke_setup):
    order_helper = my_orders_smoke_setup['order_helper']

    # User ID who owns the order. 0 for guests.
    customer_id = 0
    product_id = my_orders_smoke_setup['product_id']

    # Create an order
    info = {"line_items": [
        {
            "product_id": product_id,
            "quantity": 1
        }
    ]}
    template_order = order_helper.create_order_payload(additional_args=info)
    order_json = order_helper.create_order(payload=template_order)

    # Verify the response
    expected_products = [{'product_id': product_id}]
    order_helper.verify_order_is_created(order_json, customer_id, expected_products)


@pytest.mark.regression
@pytest.mark.parametrize("new_status",
                         [
                             pytest.param('cancelled', marks=[pytest.mark.tcid_u1, pytest.mark.regression]),
                             pytest.param('pending', marks=[pytest.mark.tcid_u2, pytest.mark.regression]),
                             pytest.param('on-hold', marks=[pytest.mark.tcid_u3, pytest.mark.regression]),
                         ])
def test_update_order_status(new_status):
    # create a new order
    order_helper = OrdersHelper()
    order_dao = OrdersDAO()
    template_order = order_helper.create_order_payload()
    order_json = order_helper.create_order(payload=template_order)
    curr_status = order_json['status']

    status_list = ['auto-draft', 'pending', 'processing', 'on-hold', 'completed',
                   'cancelled', 'refunded', 'failed', 'checkout-draft']
    if curr_status == new_status:
        new_status = [s for s in status_list if s != curr_status][0]


    # update order status
    order_id = order_json['id']

    # retrieve order status in db
    order_db_status_before = order_dao.get_order_table_data("posts", "ID", order_id)
    assert order_db_status_before[0]['post_status'] == f"wc-{curr_status}"

    # update the status
    payload = {"status": new_status}
    order_helper.update_order(order_id=order_id, payload=payload)

    # get order information
    order_after_update = order_helper.retrieve_order(order_id=order_id)

    # verify new orders status
    assert order_after_update['status'] == new_status, \
        f"status >>> Expected: '{new_status} Actual: {order_after_update['status']}'"

    # verify that order status updated in db
    order_db_status_after = order_dao.get_order_table_data("posts", "ID", order_id)
    assert order_db_status_after[0]['post_status'] == f"wc-{new_status}"


@pytest.mark.regression
def test_update_order_status_to_an_invalid_value():
    new_status = 'invalid_status'

    # create new order
    order_helper = OrdersHelper()
    template_order = order_helper.create_order_payload()
    order_json = order_helper.create_order(payload=template_order)
    order_id = order_json['id']

    # update the status
    payload = {"status": new_status}
    res_api = order_helper.update_order(order_id, payload=payload, expected_status_code=400)

    assert res_api['code'] == 'rest_invalid_param', \
        f"Code >>> Expected: 'rest_invalid_param' Actual: {res_api['code']}"

    assert res_api['message'] == 'Invalid parameter(s): status', \
        f"Message >>> Expected: 'rest_invalid_param' Actual: {res_api['message']}"


@pytest.mark.regression
def test_update_order_customer_note():
    # create a new order
    order_helper = OrdersHelper()
    template_order = order_helper.create_order_payload()
    order_json = order_helper.create_order(payload=template_order)
    order_id = order_json['id']

    # update order with a customer note
    rand_string = generate_random_string(40)
    info = {"customer_note": rand_string}
    order_helper.update_order(order_id, payload=info)

    # # verify the note in the order info api
    new_order_info = order_helper.retrieve_order(order_id)
    assert new_order_info['customer_note'] == rand_string, \
        f"Customer note >>>  Expected: {rand_string}, Actual: {new_order_info['customer_note']}"


@pytest.mark.regression
def test_apply_valid_coupon_to_order(my_coupon_setup):
    """
    Validates when x% coupon is applied to an order, the 'total' amount is reduced by x%
    """

    # create payload and make call to create order
    order_helper = OrdersHelper()

    order_payload_addition = {
        "line_items": [{"product_id": my_coupon_setup['product_id'], "quantity": 1}],
        "coupon_lines": [{"code": my_coupon_setup['coupon_code']}],
        "shipping_lines": [{"method_id": "flat_rate", "method_title": "Flat Rate", "total": "0.00"}]
    }

    template_order = order_helper.create_order_payload()
    payload = dict()
    payload.update(template_order)
    payload.update(order_payload_addition)
    res_order = order_helper.create_order(payload=payload)

    # calculate expected total price based on coupon and product price
    expected_total = float(my_coupon_setup['product_price']) \
                     - (float(my_coupon_setup['product_price']) * (float(my_coupon_setup['discount_pct']) / 100))

    # get total from order response and verify
    total = round(float(res_order['total']), 2)
    expected_total = round(expected_total, 2)

    assert total == expected_total, \
        f"Order total after applying coupon >>> Expected cost: {expected_total}, Actual: {total}"


@pytest.mark.regression
def test_create_order_with_invalid_email(my_orders_smoke_setup):
    order_helper = my_orders_smoke_setup['order_helper']
    product_id = my_orders_smoke_setup['product_id']

    # data with invalid email address
    info = {"billing": {
        "email": "notGoodEmailAddr.com"
    },
        "line_items": [
            {
                "product_id": my_orders_smoke_setup['product_id']
            }
        ]
    }
    # get the existing sales count for the product
    product_dao = ProductsDAO()
    table_data = product_dao.get_product_table_data("wc_product_meta_lookup", "product_id", product_id)
    sales_count_before = table_data[0]['total_sales']

    # create the order payload and make the call
    payload = order_helper.create_order_payload(additional_args=info)
    res_api = order_helper.create_order(payload=payload, expected_status_code=400)


    assert res_api['code'] == "rest_invalid_param", \
        f"Response code >>> Expected: rest_invalid_param, Actual: {res_api['code']}"

    assert res_api['message'] == "Invalid parameter(s): billing", \
        f"Response message >>> Expected: Invalid parameter(s): billing, Actual: {res_api['message']}"

    # assert no change registered in db for the sales count
    product_dao = ProductsDAO()
    table_data = product_dao.get_product_table_data("wc_product_meta_lookup", "product_id", product_id)
    sales_count_after = table_data[0]['total_sales']
    assert sales_count_before == sales_count_after, \
        f"sales_count should not have changed"


@pytest.mark.skip
def test_delete_an_order_and_verify_deletion():
    pass
