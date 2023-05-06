import string

import pytest
import logging as logger
import random
import pdb
from automation_code.src.utilities import generic_utility
from automation_code.src.helpers.customers_helper import CustomerHelper
from automation_code.src.dao.customers_dao import CustomersDAO
from automation_code.src.utilities.requests_utility import RequestsUtility


@pytest.mark.smoke
def test_retrieve_all_customers():
    req_utility = RequestsUtility()
    res_api = req_utility.get('customers')

    assert res_api, f"Response of list all customers is empty."


@pytest.mark.smoke
def test_create_customer_only_email_password():

    logger.info("TEST: Create new customer with email and password only.")

    user_info = generic_utility.generate_random_email_and_password()
    email = user_info['email']
    # password = user_info['password']

    # make the api call to create a customer
    customer_obj = CustomerHelper()
    customer_api_info = customer_obj.create_customer(email=email)

    # verify email and first name in the response
    assert customer_api_info['email'] == email, \
        f"Create customer api return wrong email. Email: {email}"

    # verify customer is created in database
    customer_dao = CustomersDAO()
    customer_db_info = customer_dao.get_customer_by_email(email)

    assert customer_db_info[0]['user_registered'], \
        f"User registration date is not found in the db .... "

    id_in_api = customer_api_info['id']
    id_in_db = customer_db_info[0]['ID']
    assert id_in_api == id_in_db, \
        f'Create customer api: "id" not same as "ID" in database' \
                                  f'Email: {email}'


@pytest.mark.smoke
def test_retrieve_customer_by_id():

    # retrieve a customer from db
    customer_dao = CustomersDAO()
    sample_customer_db = customer_dao.get_random_customer_from_db()
    sample_customer_id = sample_customer_db[0]['ID']

    # retrieve the customer from api
    customer_helper = CustomerHelper()
    sample_customer_api = customer_helper.get_customer_by_id(sample_customer_id)

    # verify that details match
    assert sample_customer_db[0]['user_email'] == sample_customer_api['email'], \
        f"Emails does not match between db and api data. Customer Id: {sample_customer_id}"


@pytest.mark.regression
# @pytest.mark.test112
def test_create_customer_fails_existing_email():

    # get existing email from db
    customer_dao = CustomersDAO()
    existing_cust = customer_dao.get_random_customer_from_db()
    existing_email = existing_cust[0]['user_email']

    # make the api call to create a customer with an existing email
    req_utility = RequestsUtility()
    payload = {"email": existing_email, "password": "Password1"}
    customer_api = req_utility.post(endpoint='customers', payload=payload, expected_status_code=400)

    # verify the error code
    assert customer_api['code'] == 'registration-error-email-exists', \
            f"Expected error code: 'registration-error-email-exists', " \
                f"Actual: {customer_api['code']}"


@pytest.mark.regression
def test_update_customer_details():

    # retrieve a customer from users table
    customer_dao = CustomersDAO()
    existing_customer = customer_dao.get_random_customer_from_db()
    customer_id = existing_customer[0]['ID']

    # get the users first_name in customer_lookup table
    customer_db_before = customer_dao.get_customer_by_id(customer_id)
    first_name_before = customer_db_before[0]['first_name']
    pdb.set_trace()

    # update the customer details using api
    customer_helper = CustomerHelper()
    rnd_first_name = ''.join(random.choices(string.ascii_lowercase, k=10))
    customer_helper.update_customer_details(customer_id, first_name=rnd_first_name)

    # get the users first_name in customer_lookup table again
    customer_db_after = customer_dao.get_customer_by_id(customer_id)
    first_name_after = customer_db_after[0]['first_name']
    pdb.set_trace()

    # verify that changes reflected in db
    assert first_name_after == rnd_first_name
    assert first_name_before != first_name_after

def test_delete_an_existing_customer():

    # retrieve a customer from users table
    # delete the customer using api
    # verify the deletion using api and also in db
    pass

