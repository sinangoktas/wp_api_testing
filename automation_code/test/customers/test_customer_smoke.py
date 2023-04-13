import pytest
import pdb
import logging as logger
from automation_code.src.utilities import generic_utility
from automation_code.src.helpers.customers_helper import CustomerHelper
from automation_code.src.dao.customers_dao import CustomersDAO
from automation_code.src.utilities.requests_utility import RequestsUtility

@pytest.mark.customers_smoke
@pytest.mark.tcid01
def test_create_customer_only_email_password():

    logger.info("TEST: Create new customer with email and password only.")

    user_info = generic_utility.generate_random_email_and_password()
    email = user_info['email']
    password = user_info['password']

    # make the call
    customer_obj = CustomerHelper()
    customer_api_info = customer_obj.create_customer(email=email, password=password)

    # verify email and first name in the response
    assert customer_api_info['email'] == email, f"Create customer api return wrong email. Email: {email}"
    assert customer_api_info['first_name'] == '', f"Create customer api returned value for first_name" \
                                              f"but it should be empty. "

    # # verify customer is created in database
    customer_dao = CustomersDAO()
    customer_db_info = customer_dao.get_customer_by_email(email)

    id_in_api = customer_api_info['id']
    id_in_db = customer_db_info[0]['ID']
    assert id_in_api == id_in_db, f'Create customer response "id" not same as "ID" in database.' \
                                  f'Email: {email}'

@pytest.mark.customers_smoke
@pytest.mark.tcid02
def test_get_all_customers():

    req_utility = RequestsUtility()
    res_api = req_utility.get('customers')

    assert res_api, f"Response of list all customers is empty."


@pytest.mark.customers_smoke
@pytest.mark.tcid03
def test_create_customer_fail_for_existing_email():

    # get existing email from db
    customer_dao = CustomersDAO()
    existing_cust = customer_dao.get_random_customer_from_db()
    existing_email = existing_cust[0]['user_email']

    # # call the api
    req_utility = RequestsUtility()
    payload = {"email": existing_email, "password": "Password1"}
    customer_api = req_utility.post(endpoint='customers', payload=payload, expected_status_code=400)

    assert customer_api['code'] == 'registration-error-email-exists', f"Create customer with" \
       f"existing user error 'code' is not correct. Expected: 'registration-error-email-exists', " \
        f"Actual: {customer_api['code']}"