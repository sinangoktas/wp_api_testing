from automation_code.src.utilities.generic_utility import generate_random_coupon_code, generate_random_string
from automation_code.src.helpers.coupons_helper import CouponsHelper
from automation_code.src.utilities.requests_utility import RequestsUtility

import pytest
import random
import logging as logger

pytestmark = [pytest.mark.regression, pytest.mark.coupons]

@pytest.mark.parametrize("discount_type",
                         [
                             pytest.param(None, marks=[pytest.mark.tcid_c1, pytest.mark.regression]),
                             pytest.param('percent', marks=[pytest.mark.tcid_c2]),
                             pytest.param('fixed_product', marks=[pytest.mark.tcid_c3]),
                             pytest.param('fixed_cart', marks=[pytest.mark.tcid_c4]),
                         ])
def test_create_coupon_percent_discount_type(my_setup, discount_type):
    """
    Creates a coupon with given 'discount type' verify the coupon is created.
    """

    logger.info("Testing create coupon api for 50% off coupon.")

    # one of the tests is for not sending discount type and verify the default is used,
    # is if None is given check for default
    expected_discount_type = discount_type if discount_type else 'fixed_cart'

    pct_off = str(random.randint(50, 90)) + ".00"
    coupon_code = generate_random_coupon_code(suffix="tcid_c2", length=5)

    # get the helper object
    coupon_helper = my_setup['coupon_helper']

    # prepare data and call api
    payload = dict()
    payload['code'] = coupon_code
    payload['amount'] = pct_off
    if discount_type:
        payload['discount_type'] = discount_type
    res_coupon = coupon_helper.create_coupon(payload=payload)
    coupon_id = res_coupon['id']

    # verify coupon is actually created by doing a retrieve
    res_coupon_retrieve = coupon_helper.retrieve_coupon(coupon_id)

    # verify that in api response
    assert res_coupon_retrieve['amount'] == pct_off, \
        f"Amount -> Expected: {pct_off}, Actual: {res_coupon_retrieve['amount']}."

    assert res_coupon_retrieve['code'] == coupon_code.lower(), \
        f"Code -> Expected: {coupon_code.lower()}, Actual: {res_coupon_retrieve['code']}."

    assert res_coupon_retrieve['discount_type'] == expected_discount_type, \
        f"Discount Type -> Expected: {expected_discount_type} Actual: {res_coupon_retrieve['discount_type']}."


@pytest.mark.tcid_c5
@pytest.mark.regression
def test_create_coupon_with_invalid_discount_type():
    """
    Verifies using a random string in 'discount_type' of create order will fail with correct error message.
    """

    logger.info("Testing create coupon api for with invalid 'discount_type'.")

    # prepare data and call api
    payload = dict()
    payload['code'] = generate_random_coupon_code(suffix="tcid_c5", length=5)
    payload['amount'] = str(random.randint(50, 90)) + ".00"
    payload['discount_type'] = generate_random_string()
    res_coupon = RequestsUtility().post('coupons', payload=payload, expected_status_code=400)

    assert res_coupon['code'] == 'rest_invalid_param', \
        f"Code > Actual: {res_coupon['code']}', Expected: 'rest_invalid_param' "

    assert res_coupon['message'] == 'Invalid parameter(s): discount_type', \
        f"Message > Actual: {res_coupon['message']}', Expected: 'Invalid parameter(s): discount_type',"