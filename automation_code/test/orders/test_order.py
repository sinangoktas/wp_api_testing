import pdb

import pytest
import random
from automation_code.src.dao.products_dao import ProductsDAO
from automation_code.src.dao.orders_dao import OrdersDAO
from automation_code.src.helpers.orders_helper import OrdersHelper
from automation_code.src.helpers.customers_helper import CustomerHelper
from automation_code.src.helpers.products_helper import ProductsHelper
from automation_code.src.utilities.requests_utility import RequestsUtility
from automation_code.src.utilities.generic_utility import generate_random_string

# TODO think of how to incorporate this into a utility method that can be usable for all services
# TODO And check if the new approach can deprecate the create_order_payload.json
@pytest.fixture(scope='module')
def my_orders_smoke_setup():
    product_dao = ProductsDAO()
    rand_product = product_dao.get_random_product_from_db("posts")
    product_id = rand_product[0]['ID']
    order_helper = OrdersHelper()
    info = {'product_id': product_id,
            'order_helper': order_helper}

    return info


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
    order_json = order_helper.create_order(additional_args=info)

    # Verify the response
    expected_products = [{'product_id': product_id}]
    order_helper.verify_order_is_created(order_json, customer_id, expected_products)


@pytest.mark.smoke
def test_create_paid_order_registered_customer(my_orders_smoke_setup):
    # create helper objects
    order_helper = my_orders_smoke_setup['order_helper']
    customer_helper = CustomerHelper()

    # prepare for the order: customer and product
    cust_info = customer_helper.create_customer()
    customer_id = cust_info['id']
    product_id = my_orders_smoke_setup['product_id']

    info = {"line_items": [
        {
            "product_id": product_id,
            "quantity": 1
        }
    ],
        "customer_id": customer_id
    }
    order_json = order_helper.create_order(additional_args=info)

    # # verify response
    expected_products = [{'product_id': product_id}]
    order_helper.verify_order_is_created(order_json, customer_id, expected_products)


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
    order_json = order_helper.create_order()
    curr_status = order_json['status']

    status_list = ['auto-draft', 'pending', 'processing', 'on-hold', 'completed', 'cancelled', 'refunded', 'failed', 'checkout-draft']
    if curr_status == new_status:
        new_status = [s for s in status_list if s != curr_status][0]


    # update order status
    order_id = order_json['id']

    # retrieve order status in db
    order_db_status_before = order_dao.get_order_table_data("posts", "ID", order_id)
    assert order_db_status_before[0]['post_status'] == f"wc-{curr_status}"

    # update the status
    order_helper.update_order(order_id, status=new_status)

    # get order information
    new_order_info = order_helper.retrieve_order(order_id)

    # verify new orders status
    assert new_order_info['status'] == new_status, f"Updated order status to '{new_status}'," \
                                                   f"but order is still '{new_order_info['status']}'"

    # verify that order status updated in db
    order_db_status_after = order_dao.get_order_table_data("posts", "ID", order_id)
    assert order_db_status_after[0]['post_status'] == f"wc-{new_status}"


@pytest.mark.regression
def test_update_order_status_to_an_invalid_value():
    new_status = 'invalid_status'

    # create new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    # update the status
    # res_api = order_helper.update_order(order_id, expected_status_code=400, status=new_status)
    payload = {"status": new_status}
    request_utility = RequestsUtility()
    res_api = request_utility.put(f"orders/{order_id}", payload=payload, expected_status_code=400)

    assert res_api['code'] == 'rest_invalid_param', f"Code > Expected: 'rest_invalid_param' Actual: {res_api['code']}"
    assert res_api['message'] == 'Invalid parameter(s): status', f"Message > Expected: 'rest_invalid_param' Actual: {res_api['message']}"


@pytest.mark.regression
def test_update_order_customer_note():
    # create a new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    # update order with a customer note
    rand_string = generate_random_string(40)
    info = {"customer_note": rand_string}
    order_helper.update_order(order_id, **info)

    # # verify the note in the order info api
    new_order_info = order_helper.retrieve_order(order_id)
    assert new_order_info['customer_note'] == rand_string, f"Customer note >  Expected: {rand_string}, \
                                                                        Actual: {new_order_info['customer_note']}"

@pytest.fixture(scope='module')
def my_setup_teardown():
    # hard code a 50% coupon from wp_admin > woocommerce
    coupon_code = 'kecsetcid16'
    discount_pct = '50.00'

    # get a random product for order
    rand_products = ProductsHelper().list_products()
    rand_product = random.choice(rand_products)

    info = dict()
    info['order_helper'] = OrdersHelper()
    info['coupon_code'] = coupon_code
    info['discount_pct'] = discount_pct
    info['product_id'] = rand_product['id']
    info['product_price'] = rand_product['price']

    return info

@pytest.mark.regression
def test_apply_valid_coupon_to_order(my_setup_teardown):
    """
    Validates when x% coupon is applied to an order, the 'total' amount is reduced by x%
    """

    # create payload and make call to create order
    order_helper = OrdersHelper()

    order_payload_addition = {
        "line_items": [{"product_id": my_setup_teardown['product_id'], "quantity": 1}],
        "coupon_lines": [{"code": my_setup_teardown['coupon_code']}],
        "shipping_lines": [{"method_id": "flat_rate", "method_title": "Flat Rate", "total": "0.00"}]
    }

    res_order = order_helper.create_order(additional_args=order_payload_addition)

    # calculate expected total price based on coupon and product price
    expected_total = float(my_setup_teardown['product_price']) \
                     - (float(my_setup_teardown['product_price']) * (float(my_setup_teardown['discount_pct']) / 100))

    # get total from order response and verify
    total = round(float(res_order['total']), 2)
    expected_total = round(expected_total, 2)

    assert total == expected_total, f"Order total after applying coupon > Expected cost: {expected_total}, Actual: {total}"

@pytest.mark.regression
def test_create_order_with_invalid_email(my_orders_smoke_setup):
    order_helper = my_orders_smoke_setup['order_helper']
    product_id = my_orders_smoke_setup['product_id']

    # data with invalid email address
    info = {"billing": {
        "email": "thisIsNotAgoodEmailAdress.com"
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

    # create the order payload
    payload = order_helper.create_order_payload(additional_args=info)

    requests_utility = RequestsUtility()
    res_api = requests_utility.post('orders', payload=payload, expected_status_code=400)

    assert res_api['code'] == "rest_invalid_param", f"Response code > Expected: rest_invalid_param, Actual: {res_api['code']}"
    assert res_api['message'] == "Invalid parameter(s): billing", f"Response message > Expected: Invalid parameter(s): billing, Actual: {res_api['message']}"

    # assert no change registered in db for the sales count
    product_dao = ProductsDAO()
    table_data = product_dao.get_product_table_data("wc_product_meta_lookup", "product_id", product_id)
    sales_count_after = table_data[0]['total_sales']


    assert sales_count_before == sales_count_after, f"sales_count should not have changed"


"""
Filter the list of orders by status, and verify that the filtered list matches the details stored in the WordPress database. 
(status, another_attr and another_attr)
"""

@pytest.mark.regression
# TODO Implement
def test_delete_an_order_and_verify_deletion():
    pass
