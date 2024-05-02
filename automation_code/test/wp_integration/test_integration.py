import pdb
import pytest

from automation_code.src.helpers.products_helper import ProductsHelper
from automation_code.src.utilities.generic_utility import generate_random_string
from automation_code.src.dao.orders_dao import OrdersDAO
from automation_code.src.helpers.orders_helper import OrdersHelper
from automation_code.src.helpers.customers_helper import CustomerHelper
from automation_code.src.utilities import generic_utility
from automation_code.src.dao.products_dao import ProductsDAO

@pytest.mark.integration
@pytest.mark.regression
def test_create_a_product_add_it_to_an_order():

    # Create a new product
    product_helper = ProductsHelper()
    product_info = {
        "name": generate_random_string(7),
        "type": "simple",
        "regular_price": "11.99"
    }
    product_res = product_helper.create_product(payload=product_info)
    assert product_res['name'] == product_info['name']
    product_id = product_res["id"]

    # Add the product to an order
    order_dao = OrdersDAO()
    random_order = order_dao.get_random_order_from_db("posts", 1)
    order_id = random_order[0]["ID"]

    order_helper = OrdersHelper()
    payload = {
        "line_items": [
            {
                "product_id": product_id,
                "quantity": 1
            }
        ]
    }
    order_helper.update_order(order_id, payload=payload)

    # verify that the order contains the correct product informatio
    order_with_product = order_helper.retrieve_order(order_id)
    products_list = [(item["product_id"], item["name"]) for item in order_with_product["line_items"]]
    assert product_id, product_info["name"] in products_list


@pytest.mark.integration
@pytest.mark.regression
def test_create_paid_order_registered_customer(my_orders_smoke_setup):
    # create helper objects
    order_helper = my_orders_smoke_setup['order_helper']
    customer_helper = CustomerHelper()

    # prepare for the order: customer and product
    user_data = generic_utility.generate_random_email_and_password()
    cust_info = customer_helper.create_customer(payload=user_data)
    customer_id = cust_info['id']
    product_id = my_orders_smoke_setup['product_id']

    info = {"line_items": [
        {
            "product_id": product_id,
            "quantity": 1
        }
    ],
        "customer_id": customer_id
    }
    template_order = order_helper.create_order_payload(additional_args=info)
    order_json = order_helper.create_order(payload=template_order)

    # # verify response
    expected_products = [{'product_id': product_id}]
    order_helper.verify_order_is_created(order_json, customer_id, expected_products)


@pytest.mark.integration
@pytest.mark.sg112
def test_order_with_products_update_product():
    # create helper objects
    order_helper = OrdersHelper()
    product_helper = ProductsHelper()
    product_dao = ProductsDAO()

    random_products = product_dao.get_random_product_from_db("posts", qty=2)
    product_id_one = random_products[0]['ID']
    product_id_two = random_products[1]['ID']

    # Create an order with multiple products
    info = {"line_items": [
        {
            "product_id": product_id_one,
            "quantity": 1
        },
        {
            "product_id": product_id_two,
            "quantity": 1
        }
    ]}
    template_order = order_helper.create_order_payload(additional_args=info)
    order_json = order_helper.create_order(payload=template_order)
    order_id = order_json["id"]

    # update the details of one of the products in the order
    products_on_order = order_json["line_items"]
    product_to_update = [p for p in products_on_order if p["product_id"] == product_id_one]
    line_id = product_to_update[0]["id"]
    update_payload = {"line_items": [
        {
            "id": line_id,
            "quantity": 5
        }
    ]}

    order_helper.update_order(order_id, payload=update_payload)

    # verify updated product details on the order
    order_after_update = order_helper.retrieve_order(order_id)
    products_on_order = order_after_update["line_items"]
    updated_product = [d for d in products_on_order if d["id"] == line_id]

    found = False
    for product in updated_product:
        if product["quantity"] == 5:
            found = True
    assert found, "product update on order is not successful"