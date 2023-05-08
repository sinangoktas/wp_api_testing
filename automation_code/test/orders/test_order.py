import pdb

import pytest
import random
from automation_code.src.dao.products_dao import ProductsDAO
from automation_code.src.helpers.orders_helper import OrdersHelper
from automation_code.src.helpers.customers_helper import CustomerHelper
from automation_code.src.helpers.products_helper import ProductsHelper
from automation_code.src.utilities.generic_utility import generate_random_string


@pytest.fixture(scope='module')
def my_orders_smoke_setup():
    product_dao = ProductsDAO()
    rand_product = product_dao.get_random_product_from_db(1)
    product_id = rand_product[0]['ID']

    order_helper = OrdersHelper()

    info = {'product_id': product_id,
            'order_helper': order_helper}

    return info


@pytest.mark.smoke
def test_create_paid_order_guest_user(my_orders_smoke_setup):
    order_helper = my_orders_smoke_setup['order_helper']

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

    # make the call
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


pytest_mark = [pytest.mark.smoke, pytest.mark.regression]


@pytest.mark.parametrize("new_status",
                         [
                             pytest.param('cancelled', marks=[pytest.mark.tcid_u1, pytest.mark.regression]),
                             pytest.param('pending', marks=[pytest.mark.tcid_u2, pytest.mark.regression]),
                             pytest.param('on-hold', marks=[pytest.mark.tcid_u3, pytest.mark.regression]),
                         ])
def test_update_order_status(new_status):
    # create a new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    curr_status = order_json['status']

    status_list = ['auto-draft', 'pending', 'processing', 'on-hold', 'completed', 'cancelled', 'refunded', 'failed',
                   'checkout-draft']
    if curr_status == new_status:
        new_status = [s for s in status_list if s != curr_status][0]

    # update order status
    order_id = order_json['id']
    payload = {"status": new_status}
    order_helper.update_order(order_id, payload)

    # get order information
    new_order_info = order_helper.retrieve_order(order_id)

    # verify new orders status
    assert new_order_info['status'] == new_status, f"Updated order status to '{new_status}'," \
                                                   f"but order is still '{new_order_info['status']}'"


@pytest.mark.regression
def test_update_order_status_to_an_invalid_value():
    new_status = 'invalid_status'

    # create new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    # update the status
    res_api = order_helper.update_order(order_id, expected_status_code=400, status=new_status)

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
    order_helper.update_order(order_id, expected_status_code=200, **info)

    # # verify the note in the order info api
    new_order_info = order_helper.retrieve_order(order_id)
    assert new_order_info['customer_note'] == rand_string, f"Customer note >  Expected: {rand_string}, Actual: {new_order_info['customer_note']}"



@pytest.fixture(scope='module')
def my_setup_teardown():
    # hard code a 50% coupon from wp_admin > woocommerce
    coupon_code = 'kecsetcid16'
    discount_pct = '50.00'

    # get a random product for order
    rand_products = ProductsHelper().call_list_products()
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
                     - (float(my_setup_teardown['product_price']) * (float(my_setup_teardown['discount_pct'])/100))

    # get total from order response and verify
    total = round(float(res_order['total']), 2)
    expected_total = round(expected_total, 2)


    assert total == expected_total, f"Order total after applying coupon > Expected cost: {expected_total}, Actual: {total}"
