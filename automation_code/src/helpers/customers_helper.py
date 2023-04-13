from automation_code.src.utilities import generic_utility
from automation_code.src.utilities.requests_utility import RequestsUtility

class CustomerHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def create_customer(self, email=None, password=None, expected_status_code=None, **kwargs):
        if not email:
            credentials = generic_utility.generate_random_email_and_password()
            email = credentials['email']
        if not password:
            password = 'PassW123'

        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        create_user_json = self.requests_utility.post('customers', payload=payload, expected_status_code=201)

        return create_user_json