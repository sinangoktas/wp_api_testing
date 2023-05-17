import logging as logger
from automation_code.src.utilities.requests_utility import RequestsUtility

class ProductsHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def retrieve_product(self, product_id):
        product_api_res = self.requests_utility.get(f'products/{product_id}', expected_status_code=200)
        return product_api_res

    def create_product(self, **kwargs):
        payload = dict()
        payload.update(kwargs)
        create_product_json = self.requests_utility.post('products', payload=payload, expected_status_code=201)
        return create_product_json

    def update_product(self, product_id, **kwargs):
        payload = dict()
        payload.update(kwargs)
        update_product_json = self.requests_utility.put(f'products/{product_id}', payload=payload, expected_status_code=200)
        return update_product_json

    def list_products(self, payload=None):
        max_pages = 1000
        all_products = []
        for i in range(1, max_pages + 1):
            logger.debug(f"List products page number: {i}")

            if not payload:
                payload = {}

            if not ('per_page' in payload.keys()):
                payload['per_page'] = 100

            # add the current page number to the call
            payload['page'] = i
            rs_api = self.requests_utility.get('products', payload=payload)

            # if there is no response then stop the loop b/c there are no more products
            if not rs_api:
                break
            else:
                all_products.extend(rs_api)
        else:
            raise Exception(f"Unable to find all products after {max_pages} pages.")

        return all_products
