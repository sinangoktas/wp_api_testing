import pytest
import pdb
import logging as logger
from automation_code.src.utilities.requests_utility import RequestsUtility
from automation_code.src.dao.products_dao import ProductsDAO
from automation_code.src.helpers.products_helper import ProductsHelper
from automation_code.src.utilities.generic_utility import generate_random_string


@pytest.mark.products_smoke
@pytest.mark.tcid04
def test_get_all_products():
    req_utility = RequestsUtility()
    res_api = req_utility.get(endpoint='products')
    assert res_api, f"Get all products end point returned nothing."


@pytest.mark.products_smoke
@pytest.mark.tcid05
def test_get_product_by_id():

    # get a product (test data) from db
    rand_product = ProductsDAO().get_random_product_from_db(1)
    rand_product_id = rand_product[0]['ID']
    db_name = rand_product[0]['post_title']

    # make the call
    product_helper = ProductsHelper()
    res_api = product_helper.get_product_by_id(rand_product_id)
    api_name = res_api['name']

    # verify the response
    assert db_name == api_name, f"Get product by id returned wrong product. Id: {rand_product_id}" \
                                f"Db name: {db_name}, Api name: {api_name}"

@pytest.mark.products_smoke
@pytest.mark.tcid06
def test_create_a_simple_product():

    # generate some data
    payload = dict()
    payload['name'] = generate_random_string(20)
    payload['type'] = "simple"
    payload['regular_price'] = "10.99"

    # make the call
    product_res = ProductsHelper().call_create_product(payload)

    # verify ethe response is not empty
    assert product_res, f"Create product api response is empty. Payload: {payload}"
    assert product_res['name'] == payload['name'], f"Create product api call response has" \
       f"unexpected name. Expected: {payload['name']}, Actual: {product_res['name']}"

    # verify the product exists in db
    product_id = product_res['id']
    db_product = ProductsDAO().get_product_by_id(product_id)

    assert payload['name'] == db_product[0]['post_title'], f"Create product, title in db does not match " \
     f"name in api. DB: {db_product['post_title']}, API: {payload['name']}"