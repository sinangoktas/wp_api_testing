import pytest
from datetime import datetime, timedelta
from automation_code.src.utilities.requests_utility import RequestsUtility
from automation_code.src.dao.products_dao import ProductsDAO
from automation_code.src.helpers.products_helper import ProductsHelper
from automation_code.src.utilities.generic_utility import generate_random_string

@pytest.mark.smoke
def test_get_all_products():
    req_utility = RequestsUtility()
    res_api = req_utility.get(endpoint='products')
    assert res_api, f"Get all products end point returned nothing."


@pytest.mark.smoke
def test_get_product_by_id():

    # get a product (test data) from db
    rand_product = ProductsDAO().get_random_product_from_db(1)
    rand_product_id = rand_product[0]['ID']
    db_name = rand_product[0]['post_title']

    # retrieve the product from api
    product_helper = ProductsHelper()
    res_api = product_helper.get_product_by_id(rand_product_id)
    api_name = res_api['name']

    # verify that names matches in api and db
    assert db_name == api_name, f" Product Id: {rand_product_id} > Db name: {db_name}, Api name: {api_name}"


@pytest.mark.smoke
def test_create_a_simple_product():

    # generate some data
    payload = dict()
    payload['name'] = generate_random_string(20)
    payload['type'] = "simple"
    payload['regular_price'] = "10.99"

    # create the product using api
    product_res = ProductsHelper().create_product(payload)

    # verify that response is not empty
    assert product_res, f"Create product api response is empty. Payload: {payload}"
    assert product_res['name'] == payload['name'], f"Product name > Expected: {payload['name']}, Actual: {product_res['name']}"

    # verify that product exists in db
    product_id = product_res['id']
    db_product = ProductsDAO().get_product_by_id(product_id)

    assert payload['name'] == db_product[0]['post_title'], f"Product name > DB: {db_product['post_title']}, API: {payload['name']}"


@pytest.mark.regression
def test_list_products_with_filter_after():
    # create data
    x_days_from_today = 300
    _after_created_date = datetime.now().replace(microsecond=0) - timedelta(days=x_days_from_today)
    after_created_date = _after_created_date.isoformat()

    # make the call
    payload = dict()
    payload['after'] = after_created_date
    res_api = ProductsHelper().call_list_products(payload)
    assert res_api, f"Empty response for 'list products with filer"

    # get data from db
    db_products = ProductsDAO().get_products_created_after_given_date(after_created_date)

    # verify response match db
    assert len(res_api) == len(db_products), f"Products count after filter applied > Expected: {len(db_products)}, Actual: {len(res_api)}"

    ids_in_api = [i['id'] for i in res_api]
    ids_in_db = [i['ID'] for i in db_products]

    ids_diff = list(set(ids_in_api) - set(ids_in_db))
    assert not ids_diff, f"Product ids are different in api response and db"