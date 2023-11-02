import random

import httpx
from config.core import settings
from fastapi.responses import Response
from lib.test import TestRouter, test_logger
from router.endpoints.orders import router


def get_key() -> str:
    response: list = httpx.get(settings.PRODUCT_API).json()
    options = [item for item in response if int(item["quantity"]) > 2]
    sample = random.choice(options)
    return sample["id"]


id = "pk"
name = "orders"
example = {
    "product_id": get_key(),
    "quantity": random.randint(1, 2),
}

orders_tests = TestRouter(name, example, router, id_field=id)


@test_logger
def test_get() -> None:
    data: dict = orders_tests.initialise_example()
    path: str = f"{orders_tests.endpoint}/{data.get(orders_tests.id_field)}"
    response: Response = orders_tests.client.get(path)

    # Adjust the status value from "pending" to "completed"
    data["status"] = "completed"
    """
    NOTE - This is adjustment is just for a proof of concept and
    wouldn't be necessary for a production level microservice testings
    """

    assert response.status_code == 200
    assert response.json() == data


def custom_default_test() -> None:
    # POST
    # orders_router.test_list()

    # POST
    orders_tests.test_create()
    orders_tests.test_create_missing_field()

    # GET
    test_get()
    orders_tests.test_get_nonexisting()

    # # PUT
    # orders_router.test_update()
    # orders_router.test_update_nonexisting()

    # # DELETE
    # orders_router.test_delete()
    # orders_router.test_delete_nonexisting()


orders_tests.default = custom_default_test
