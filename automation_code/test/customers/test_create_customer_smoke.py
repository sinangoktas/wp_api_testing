import logging as logger

import pytest

from automation_code.src.utilities import generic_utility
from automation_code.src.helpers.customers_helper import CustomerHelper

@pytest.mark.tcid01
def test_create_customer_only_email_password():

    logger.info("TEST: Create new customer with email and password only.")

    user_info = generic_utility.generate_random_email_and_password()
    email = user_info['email']
    password = user_info['password']

    # make the call
    cust_obj = CustomerHelper()
    cust_api_info = cust_obj.create_customer(email=email, password=password)

    # verify email and first name in the response
    assert cust_api_info['email'] == email, f"Create customer api return wrong email. Email: {email}"
    assert cust_api_info['first_name'] == '', f"Create customer api returned value for first_name" \
                                              f"but it should be empty. "

    # # verify customer is created in database
    # cust_dao = CustomersDAO()
    # cust_info = cust_dao.get_customer_by_email(email)
    #
    # id_in_api = cust_api_info['id']
    # id_in_db = cust_info[0]['ID']
    # assert id_in_api == id_in_db, f'Create customer response "id" not same as "ID" in database.' \
    #                               f'Email: {email}'