import pytest
from automation_code.src.helpers.orders_helper import OrdersHelper
from automation_code.src.utilities.requests_utility import RequestsUtility
from automation_code.src.utilities.generic_utility import generate_random_string

pytest_mark = [pytest.mark.orders, pytest.mark.regression]


@pytest.mark.parametrize("new_status",
                         [
                             pytest.param('cancelled', marks=[pytest.mark.tcid10, pytest.mark.smoke]),
                             pytest.param('pending', marks=pytest.mark.tcid11),
                             pytest.param('on-hold', marks=pytest.mark.tcid12),
                         ])
def test_update_order_status(new_status):
    # create new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    cur_status = order_json['status']
    assert cur_status != new_status, f"Current status of order is already {new_status}. " \
                                     f"Unable to run test."

    # update the status
    order_id = order_json['id']
    payload = {"status": new_status}
    order_helper.call_update_an_order(order_id, payload)

    # get order information
    new_order_info = order_helper.call_retrieve_an_order(order_id)

    # verify the new order status is what was updated
    assert new_order_info['status'] == new_status, f"Updated order status to '{new_status}'," \
                                                   f"but order is still '{new_order_info['status']}'"


@pytest.mark.tcid13
def test_update_order_status_to_random_string():
    new_status = 'abcdefg'

    # create new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    # update the status
    payload = {"status": new_status}
    res_api = RequestsUtility().put(f'orders/{order_id}', payload=payload, expected_status_code=400)

    assert res_api['code'] == 'rest_invalid_param', f"Update order status to random string did not have " \
                                                   f"correct code in response. Expected: 'rest_invalid_param' Actual: {res_api['code']}"

    assert res_api['message'] == 'Invalid parameter(s): status', f"Update order status to random " \
                                                                f"string did not have correct message in response. " \
                                                                f"Expected: 'rest_invalid_param' Actual: {res_api['message']}"


@pytest.mark.tcid14
def test_update_order_customer_note():
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    rand_string = generate_random_string(40)
    payload = {"customer_note": rand_string}
    order_helper.call_update_an_order(order_id, payload)

    # get order information
    new_order_info = order_helper.call_retrieve_an_order(order_id)
    assert new_order_info['customer_note'] == rand_string, f"Update order's 'customer_note' field," \
                                                           f"failed. Expected: {rand_string}, Actual: {new_order_info['customer_note']}"
