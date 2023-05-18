from automation_code.src.utilities import generic_utility
from automation_code.src.utilities.requests_utility import RequestsUtility

import base64
import pdb
import requests
from automation_code.src.utilities.credentials_utility import CredentialsUtility

class CustomerHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def retrieve_customer(self, id):
        customer_api_res = self.requests_utility.get(f'customers/{id}', expected_status_code=200)
        return customer_api_res

    def create_customer(self, email=None, **kwargs):
        payload = dict()
        if not email:
            credentials = generic_utility.generate_random_email_and_password()
            email = credentials['email']
        payload['email'] = email
        payload.update(kwargs)
        create_user_json = self.requests_utility.post('customers', payload=payload, expected_status_code=201)
        return create_user_json

    def update_customer(self, id, **kwargs):
        payload = dict()
        payload.update(kwargs)
        update_user_json = self.requests_utility.put(f'customers/{id}', payload=payload, expected_status_code=200)
        return update_user_json

    # TODO del
    # 501
    # def delete_customer(self, id, headers=None):
    # 401
    def delete_customer(self, id):
        # 401 Error
        creds = CredentialsUtility()
        params = creds.get_wc_api_keys()
        res = self.requests_utility.delete(f'customers/{id}', headers=params)
        print(res)
        print(res['code'])
        print(res['message'])

        # 501 Error
        # if not headers:
        #     username = "sinang"
        #     password = "sg024435X!"
        #     headers = {
        #         'Content-Type': 'application/json',
        #         'Authorization': f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}'
        #     }
        # res = self.requests_utility.delete(f'customers/{id}', headers=headers)
        # print(res)
        # print(res['code'])
        # print(res['message'])


