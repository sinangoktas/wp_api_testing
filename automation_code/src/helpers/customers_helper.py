import base64
import pdb

from automation_code.src.utilities import generic_utility
from automation_code.src.utilities.requests_utility import RequestsUtility

# TODO 112
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


    def get_customer_by_id(self, id, expected_status_code=200):

        customer_api_res = self.requests_utility.get(f'customers/{id}', expected_status_code)
        return customer_api_res


    def update_customer(self, id, expected_status_code, **kwargs):

        payload = dict()
        payload.update(kwargs)

        return self.requests_utility.put(f'customers/{id}', payload=payload, expected_status_code=expected_status_code)


    def delete_customer(self, id, headers=None, expected_status_code=None):

        if not expected_status_code:
            expected_status_code = 200

        if not headers:
            username = "sinang"
            password = "sg024435X!"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}'
            }

        delete_customer_res = self.requests_utility.delete(f'customers/{id}', headers, expected_status_code)
        return delete_customer_res