from automation_code.src.utilities import generic_utility
from automation_code.src.utilities.requests_utility import RequestsUtility

import base64
import pdb
import requests
from automation_code.src.utilities.credentials_utility import CredentialsUtility

class CustomerHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def retrieve_customer(self, id=None, expected_status_code=200):
        customer_api_res = self.requests_utility.get(f'customers/{id}',
                                                     expected_status_code=expected_status_code)
        return customer_api_res

    def create_customer(self, payload=None, expected_status_code=201):
        create_user_json = self.requests_utility.post('customers',
                                                      payload=payload,
                                                      expected_status_code=expected_status_code)
        return create_user_json

    def update_customer(self, id=None, payload=None, expected_status_code=200):
        update_user_json = self.requests_utility.put(f'customers/{id}',
                                                     payload=payload,
                                                     expected_status_code=expected_status_code)
        return update_user_json

    def delete_customer(self, id):
        # 401 Error
        # creds = CredentialsUtility()
        # params = creds.get_wc_api_keys()
        # res = self.requests_utility.delete(f'customers/{id}', headers=params)

        # 501 Error
        username = "sinang"
        password = "sg024435X!"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}'
        }

        self.requests_utility.delete(f'customers/{id}', headers=headers)


