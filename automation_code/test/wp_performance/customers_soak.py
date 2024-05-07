import pdb
import requests
from locust import HttpUser, task, between
from automation_code.src.helpers.customers_helper import CustomerHelper
from automation_code.src.utilities.requests_utility import RequestsUtility
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1

class WebsiteUser(HttpUser):

    # Simulate real user wait time between requests
    wait_time = between(1, 2)
    req = RequestsUtility()
    wc_creds = req.wc_creds
    host = req.base_url
    # oauth_session = None

    def on_start(self):
        """ Set up OAuth1 authentication """
        self.auth = OAuth1(self.wc_creds['wc_key'], self.wc_creds['wc_secret'])

    # @task
    # def create_customer(self):
    #     self.client.post("/wp-json/wc/v3/customers", json={
    #         "email": "user@example.com",
    #         "first_name": "John",
    #         "last_name": "Doe",
    #         "username": "john_doe",
    #         "billing": {
    #             "first_name": "John",
    #             "last_name": "Doe",
    #             "company": "",
    #             "address_1": "969 Market",
    #             "address_2": "",
    #             "city": "San Francisco",
    #             "state": "CA",
    #             "postcode": "94103",
    #             "country": "US",
    #             "email": "john.doe@example.com",
    #             "phone": "(555) 555-5555"
    #         }
    #     })

    @task
    def read_customer(self):
        try:

            response = self.client.get(f"{self.req.base_url}customers", auth=self.auth)
            print("Response status code:", response.status_code)
        except Exception as e:
            print(f"An error occurred: {e}")

    # @task
    # def update_customer(self):
    #     self.client.put("/wp-json/wc/v3/customers/123", json={
    #         "first_name": "Jane",
    #         "last_name": "Doe"
    #     })
    #
    # @task
    # def delete_customer(self):
    #     self.client.delete("/wp-json/wc/v3/customers/123")
