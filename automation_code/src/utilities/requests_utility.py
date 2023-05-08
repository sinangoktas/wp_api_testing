import base64
import pdb

from automation_code.src.configs.hosts_config import API_HOSTS
from automation_code.src.utilities.credentials_utility import CredentialsUtility

import requests
import os
import json
from requests_oauthlib import OAuth1
import logging as logger


class RequestsUtility(object):

    def __init__(self):
        self.url = None
        self.status_code = None
        self.expected_status_code = None
        self.res_json = None
        self.env = os.environ.get('ENV', 'test')
        self.base_url = API_HOSTS[self.env]
        wc_creds = CredentialsUtility.get_wc_api_keys()
        self.auth = OAuth1(wc_creds['wc_key'], wc_creds['wc_secret'])

    def assert_status_code(self):
        assert self.status_code == self.expected_status_code, f"Bad Status code." \
                                                              f"Expected {self.expected_status_code}, Actual status code: {self.status_code}," \
                                                              f"URL: {self.url}, Response Json: {self.res_json}"

    def get(self, endpoint, payload=None, headers=None, expected_status_code=200):

        if not headers:
            headers = {"Content-Type": "application/json"}

        self.url = self.base_url + endpoint
        res_api = requests.get(url=self.url, data=json.dumps(payload), headers=headers, auth=self.auth)
        self.status_code = res_api.status_code
        self.expected_status_code = expected_status_code
        self.res_json = res_api.json()
        self.assert_status_code()

        logger.debug(f"GET API response: {self.res_json}")

        return self.res_json

    def post(self, endpoint, payload=None, headers=None, expected_status_code=200):

        if not headers:
            headers = {"Content-Type": "application/json"}

        self.url = self.base_url + endpoint

        res_api = requests.post(url=self.url, data=json.dumps(payload), headers=headers, auth=self.auth)
        self.status_code = res_api.status_code
        self.expected_status_code = expected_status_code
        self.res_json = res_api.json()
        self.assert_status_code()

        logger.debug(f"POST API response: {self.res_json}")

        return self.res_json

    def put(self, endpoint, payload=None, headers=None, expected_status_code=None):

        if not headers:
            headers = {"Content-Type": "application/json"}

        self.url = self.base_url + endpoint
        res_api = requests.put(url=self.url, data=json.dumps(payload), headers=headers, auth=self.auth)
        self.status_code = res_api.status_code
        self.expected_status_code = expected_status_code
        self.res_json = res_api.json()
        self.assert_status_code()

        logger.debug(f"PUT API response: {self.res_json}")

        return self.res_json


    def delete(self, endpoint, headers=None, expected_status_code=None):

        if not headers:
            headers = {"Content-Type": "application/json"}

        self.url = self.base_url + endpoint
        res_api = requests.delete(url=self.url, headers=headers)
        self.status_code = res_api.status_code
        self.expected_status_code = expected_status_code
        self.res_json = res_api.json()
        self.assert_status_code()

        logger.debug(f"DELETE API response: {self.res_json}")

        return self.res_json
