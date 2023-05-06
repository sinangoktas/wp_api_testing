import pdb

from automation_code.src.utilities import generic_utility
from automation_code.src.utilities.requests_utility import RequestsUtility

class CustomerHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()


    def create_customer(self, email=None, **kwargs):
        if not email:
            credentials = generic_utility.generate_random_email_and_password()
            email = credentials['email']

        payload = dict()
        payload['email'] = email
        payload.update(kwargs)

        create_user_json = self.requests_utility.post('customers', payload=payload, expected_status_code=201)

        return create_user_json

    def get_customer_by_id(self, id):

        customer_api_res = self.requests_utility.get(f'customers/{id}', expected_status_code=200)
        return customer_api_res
