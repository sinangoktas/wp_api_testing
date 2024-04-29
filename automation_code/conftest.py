import pytest
import requests
from requests_oauthlib import OAuth1

from automation_code.src.dao.products_dao import ProductsDAO
from automation_code.src.helpers.orders_helper import OrdersHelper
from automation_code.src.helpers.products_helper import ProductsHelper
from automation_code.src.helpers.coupons_helper import CouponsHelper
from automation_code.src.utilities.requests_utility import RequestsUtility


@pytest.fixture(scope='module')
def my_orders_smoke_setup():
    product_dao = ProductsDAO()
    rand_product = product_dao.get_random_product_from_db("posts")
    product_id = rand_product[0]['ID']
    order_helper = OrdersHelper()
    info = {'product_id': product_id,
            'order_helper': order_helper}

    return info

@pytest.fixture(scope='module')
def my_coupon_setup():
    # hard code a 50% coupon from wp_admin > woocommerce
    coupon_code = 'kecsetcid16'
    discount_pct = '50.00'

    # get a random product for order
    product_helper = ProductsHelper()
    rand_products = product_helper.list_products()
    rand_product = random.choice(rand_products)

    info = dict()
    info['order_helper'] = OrdersHelper()
    info['coupon_code'] = coupon_code
    info['discount_pct'] = discount_pct
    info['product_id'] = rand_product['id']
    info['product_price'] = rand_product['price']

    return info


@pytest.fixture(scope='module')
def my_setup():
    info = {'coupon_helper': CouponsHelper()}

    return info


@pytest.fixture(scope="session")
def api_client_example():
    """Fixture to authenticate and return an API session."""
    session = requests.Session()

    # Assuming your API requires a POST request to authenticate
    auth_url = "https://yourapi.com/auth"
    credentials = {"username": "user", "password": "pass"}
    response = session.post(auth_url, json=credentials)

    if response.status_code == 200:
        token = response.json().get('token')
        session.headers.update({'Authorization': f'Bearer {token}'})
        session.auth = OAuth1(wc_creds['wc_key'], wc_creds['wc_secret'])
        return session
    else:
        pytest.fail("Authentication failed. Can't proceed with tests.")



# Fixture to use explicit session testing
@pytest.fixture(scope="module")
def api_client():
    session = RequestsUtility()
    return session
