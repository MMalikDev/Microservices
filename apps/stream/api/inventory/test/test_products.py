import random

from lib.test import TestRouter
from router.endpoints.products import router

id = "pk"
name = "products"
example = {
    "name": "Test",
    "price": random.randint(10, 100),
    "quantity": random.randint(10, 25),
}


products_tests = TestRouter(name, example, router, id_field=id)
