from automation_code.src.utilities.requests_utility import RequestsUtility
import logging as logger

class CouponsHelper(object):

    def __init__(self):
        self.req_utility = RequestsUtility()


    def create_coupon(self, payload):
        logger.debug("Calling 'Create Coupon'.")
        return self.req_utility.post('coupons', payload=payload, expected_status_code=201)


    def retrieve_coupon(self, coupon_id):
        logger.debug("Calling retrieve a coupon. Coupon id: {}")
        return self.req_utility.get(f'coupons/{coupon_id}')