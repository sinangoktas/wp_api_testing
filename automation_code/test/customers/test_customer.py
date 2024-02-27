import string

import pytest
import logging as logger
import random
import pdb
from automation_code.src.utilities import generic_utility
from automation_code.src.helpers.customers_helper import CustomerHelper
from automation_code.src.dao.customers_dao import CustomersDAO
from automation_code.src.utilities.requests_utility import RequestsUtility

pytestmark = pytest.mark.customer


@pytest.mark.smoke
def test_retrieve_all_customers():
    req_utility = RequestsUtility()
    res_api = req_utility.get('customers')

    assert res_api, f"Response of list all customers is empty."


@pytest.mark.smoke
def test_create_customer_only_email_password():
    # if you want to log a test description
    logger.info("TEST: Create new customer with email and password only.")

    # create user's credentials
    user_info = generic_utility.generate_random_email_and_password()
    email = user_info['email']

    # make the api call to create the user
    customer_obj = CustomerHelper()
    customer_api_info = customer_obj.create_customer(email=email)

    # verify email and first name in the response
    assert customer_api_info['email'] == email, f"Create customer api return wrong email. Email: {email}"

    # verify customer is created in database
    customer_dao = CustomersDAO()
    customer_db_info = customer_dao.get_customer_table_data("users", "user_email", f"'{email}'")
    assert customer_db_info[0]['user_registered'], f"User registration date is not found in the db .... "

    id_in_api = customer_api_info['id']
    id_in_db = customer_db_info[0]['ID']
    assert id_in_api == id_in_db,  f'Create customer api: "id" not same as "ID" in database Email: {email}'


@pytest.mark.smoke
def test_retrieve_customer_by_id():
    # retrieve a customer from db
    customer_dao = CustomersDAO()
    sample_customer_db = customer_dao.get_random_customer_from_db("users")
    sample_customer_id = sample_customer_db[0]['ID']

    # retrieve the customer from api
    customer_helper = CustomerHelper()
    sample_customer_api = customer_helper.retrieve_customer(sample_customer_id)

    # verify that details match
    assert sample_customer_db[0]['user_email'] == sample_customer_api['email'], f"Emails does not match between db and api data. " \
                                                                                f"Customer Id: {sample_customer_id}"


@pytest.mark.regression
def test_create_customer_fails_existing_email():
    # get existing email from db
    customer_dao = CustomersDAO()
    existing_cust = customer_dao.get_random_customer_from_db("users")
    existing_email = existing_cust[0]['user_email']

    # make the api call to create a customer with an existing email
    req_utility = RequestsUtility()
    payload = {"email": existing_email, "password": "Password1"}
    customer_api = req_utility.post(endpoint='customers', payload=payload, expected_status_code=400)

    # verify the error code
    assert customer_api['code'] == 'registration-error-email-exists', f"Expected error code: 'registration-error-email-exists'" \
                                                                      f" Actual: {customer_api['code']}"


@pytest.mark.regression
def test_update_customer_details():
    # retrieve a customer from users table
    customer_dao = CustomersDAO()
    existing_customer = customer_dao.get_random_customer_from_db("users")
    customer_id = existing_customer[0]['ID']

    # get the users first_name in customer_lookup table
    customer_db_before = customer_dao.get_customer_table_data("wc_customer_lookup", "user_id", customer_id)
    first_name_before = customer_db_before[0]['first_name']

    # update the customer details using api
    customer_helper = CustomerHelper()
    rnd_first_name = ''.join(random.choices(string.ascii_lowercase, k=10))
    customer_helper.update_customer(customer_id, first_name=rnd_first_name)

    # get the users first_name in customer_lookup table again
    customer_db_after = customer_dao.get_customer_table_data("wc_customer_lookup", "user_id", customer_id)
    first_name_after = customer_db_after[0]['first_name']

    # verify that changes reflected in db
    assert first_name_after == rnd_first_name
    assert first_name_before != first_name_after, f"first_name >>> should have been updated with {rnd_first_name}"

# TODO Needs investigating ... delete permission issue
@pytest.mark.skip
@pytest.mark.regression
def test_delete_an_existing_customer():

    # create a customer
    customer_helper = CustomerHelper()
    customer = customer_helper.create_customer()
    customer_id = customer['id']

    # This block is not working. Change the response code and see the error message of ....
    """
    Response Json: {'code': 'woocommerce_rest_trash_not_supported', 'message': 'Customers do not support trashing.'
    """
    # delete the customer using api
    res = customer_helper.delete_customer(customer_id)
    print(res['code'])
    print(res['message'])

    # verify the deletion using api and also in db

    assert 1 == 2, f"Done ........................"