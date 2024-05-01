import pdb

import pytest
import random
from datetime import datetime, timedelta
from automation_code.src.utilities.requests_utility import RequestsUtility
from automation_code.src.dao.products_dao import ProductsDAO
from automation_code.src.helpers.products_helper import ProductsHelper
from automation_code.src.utilities.generic_utility import generate_random_string

pytestmark = pytest.mark.product


@pytest.mark.smoke
def test_get_all_products():
    req_utility = RequestsUtility()
    res_api = req_utility.get(endpoint='products')
    assert res_api, f"Get all products end point returned nothing."


@pytest.mark.smoke
def test_get_product_by_id():
    # get a product (test data) from db
    rand_product = ProductsDAO().get_random_product_from_db("posts")
    rand_product_id = rand_product[0]['ID']
    db_name = rand_product[0]['post_title']

    # retrieve the product from api
    product_helper = ProductsHelper()
    res_api = product_helper.retrieve_product(product_id=rand_product_id)
    api_name = res_api['name']

    # verify that names matches in api and db
    assert db_name == api_name, f" Product Id: {rand_product_id} >>> Db name: {db_name}, Api name: {api_name}"


@pytest.mark.regression
def test_create_a_simple_product():
    additional_args = {"name": generate_random_string(10),
                       "type": "simple",
                       "regular_price": "10.99"
                       }

    # create the product using api
    product_res = ProductsHelper().create_product(payload=additional_args)

    # verify that response is not empty
    assert product_res, \
        f"Create product api response is empty. Payload: {additional_args}"

    assert product_res['name'] == additional_args['name'], \
        f"Product name >>> Expected: {additional_args['name']}, Actual: {product_res['name']}"

    # verify that product exists in db
    product_id = product_res['id']
    db_product = ProductsDAO().get_product_table_data("posts", "ID", product_id)

    assert additional_args['name'] == db_product[0][
        'post_title'], f"Product name > DB: {db_product['post_title']}, API: {additional_args['name']}"


@pytest.mark.regression
def test_list_products_with_filter_after():
    # create data
    x_days_from_today = 300
    _after_created_date = datetime.now().replace(microsecond=0) - timedelta(days=x_days_from_today)
    after_created_date = _after_created_date.isoformat()

    # retrieve the products applying filter
    payload = dict()
    payload['after'] = after_created_date
    res_api = ProductsHelper().list_products(payload=payload)
    assert res_api, \
        f"Empty response for 'list products with filer"

    # get data from db for the same filter value
    db_products = ProductsDAO().get_products_created_after_given_date(after_created_date)

    # verify that api response matches db data
    assert len(res_api) == len(db_products), \
        f"Products count after filter applied >>> Expected: {len(db_products)}, Actual: {len(res_api)}"

    ids_in_api = [i['id'] for i in res_api]
    ids_in_db = [i['ID'] for i in db_products]
    ids_diff = list(set(ids_in_api) - set(ids_in_db))
    assert not ids_diff, \
        f"Product ids are different in api response and db"


# for this test the 'sale_price' of the product must be empty. If product has sale price, updating the 'regular_price'
# does not update the 'price'. So get a bunch of products and loop until you find one that is not on sale. If all in
# the list are on sale then take random one and update the sale price
@pytest.mark.regression
def test_update_regular_price_should_update_price():
    """
    Verifies updating the 'regular_price' field should automatically update the 'price' field.
    """

    # create helper objects and get random product from db
    product_helper = ProductsHelper()
    product_dao = ProductsDAO()
    rand_products = product_dao.get_random_product_from_db("posts", 10)
    for product in rand_products:
        product_id = product['ID']
        product_data = product_helper.retrieve_product(product_id=product_id)
        if product_data['on_sale']:
            continue
        else:
            break
    else:
        # take a random product and make it not on sale by setting sale_price=''
        test_product = random.choice(rand_products)
        product_id = test_product['ID']
        payload = {'sale_price': ''}
        product_helper.update_product(product_id=product_id, payload=payload)

    # update to 'regular_price'
    new_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
    payload = {'regular_price': new_price}
    res_update = product_helper.update_product(product_id=product_id, payload=payload)

    # verify the response has the 'price' and 'regular_price' has updated and 'sale_price' is not updated
    assert res_update['price'] == new_price, \
        f"Price > Actual: {res_update['price']}, Expected: {new_price}"

    assert res_update['regular_price'] == new_price, \
        f"'regular_price' > Actual: ={res_update['price']}, Expected: {new_price}"

    # get the product after the update and verify response
    rs_product = product_helper.retrieve_product(product_id)
    assert rs_product['price'] == new_price, \
        f"Price > Actual: {rs_product['price']}, Expected: {new_price}"

    assert rs_product['regular_price'] == new_price, \
        f"'regular_price' > Actual: ={rs_product['price']}, Expected: {new_price}"


@pytest.mark.regression
def test_adding_sale_price_should_set_on_sale_flag_true():
    """
    When the sale price of a product is updated, then it should set the field 'on_sale' = True
    """

    # first get a product from db that is not on sale
    product_helper = ProductsHelper()
    product_dao = ProductsDAO()
    rand_product = product_dao.get_random_products_that_are_not_on_sale(1)
    product_id = rand_product[0]['ID']

    table_data_before = product_dao.get_product_table_data("wc_product_meta_lookup", "product_id", product_id)
    assert table_data_before[0]['onsale'] == 0

    # first check the status is False to start with
    original_info = product_helper.retrieve_product(product_id=product_id)
    assert not original_info['on_sale'], \
        "Product should not be on_sale already"
    assert original_info['regular_price'], \
        "regular_price should not be empty"

    sale_price = round(float(original_info['regular_price']) * 0.75, 2)
    payload = {'sale_price': str(sale_price)}
    product_helper.update_product(product_id, payload=payload)

    # get the product sale price is updated
    after_info = product_helper.retrieve_product(product_id=product_id)
    assert after_info['on_sale'], \
        f"'on_sale' should have been set to True but found False"

    assert after_info['sale_price'] == str(sale_price), \
        f"sale_price >> Expected: {sale_price}, Actual: {after_info['sale_price']}"

    table_data_after = product_dao.get_product_table_data("wc_product_meta_lookup", "product_id", product_id)
    assert table_data_after[0]['onsale'] == 1


@pytest.mark.regression
def test_update_on_sale_field_by_updating_sale_price():
    """
    Two test case.
    First case update the 'sale_price > 0' and verify the field changes to 'on_sale=True'.
    Second case update the 'sale_price=""' and verify the field changes to 'on_sale=False'.
    """

    product_helper = ProductsHelper()

    # create product for the tests and verify the product has on_sale=False
    regular_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))

    payload = {"name": generate_random_string(10),
                       "type": "simple",
                       "regular_price": regular_price
                       }

    product_info = product_helper.create_product(payload=payload)
    product_id = product_info['id']
    assert not product_info['on_sale'], \
        f"'on_sale' should have value False for Newly created product"

    assert not product_info['sale_price'], \
        f"'sale_price' should have no value for Newly created product"

    # update the 'sale_price' and verify the 'on_sale' is set to True
    sale_price = float(regular_price) * .75
    payload = {'sale_price': str(sale_price)}
    product_helper.update_product(product_id=product_id, payload=payload)
    product_after_update = product_helper.retrieve_product(product_id)
    assert product_after_update['on_sale'], \
        f"'on_sale' did not set to 'True' for Product id: {product_id}"

    # update the sale_price to empty string and verify the 'on_sale is set to False
    payload = {'sale_price': ''}
    product_helper.update_product(product_id=product_id, payload=payload)
    product_after_update = product_helper.retrieve_product(product_id=product_id)
    assert not product_after_update['on_sale'], \
        f"'on_sale' did not set to 'False' for Product id: {product_id}"

    # assert that name of the product matches between api and db
    product_dao = ProductsDAO()
    product_name_api = [p for p in product_helper.list_products() if p['name'] == product_after_update['name']][0][
        'name']
    product_name_db = product_dao.get_product_table_data("posts", "ID", product_id)[0]['post_title']

    assert product_name_api == product_name_db


@pytest.mark.regression
def test_product_categories_validate_in_db():
    # get a random product from db
    product_dao = ProductsDAO()
    rand_product = product_dao.get_random_product_from_db("posts")
    product_id = rand_product[0]['ID']

    # fetch the categories from api
    product_helper = ProductsHelper()
    product = product_helper.retrieve_product(product_id=product_id)
    product_categories = product['categories']
    categories_list_api = [c['id'] for c in product_categories]

    # verify the categories for the product in db
    product_data_db = product_dao.get_product_table_data('term_relationships', 'object_id', product_id)
    categories_list_db = [c['term_taxonomy_id'] for c in product_data_db]

    match_list = [id for id in categories_list_api if id in categories_list_db]
    assert len(match_list) >= 1, \
        f"There should be at least one category matches between api and db data for a product"


@pytest.mark.skip
def test_delete_a_product_and_verify_deletion():
    pass
