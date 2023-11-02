import json
import time

import httpx
from config.core import settings
from db.setup import database
from fastapi import status
from fastapi.encoders import jsonable_encoder
from models.orders import Order, OrderStatus


# ---------------------------------------------------------------------- #
# Query Handling
# ---------------------------------------------------------------------- #
def pagination(data: list, page: int = 1, limit: int = 100) -> list:
    startIndex = (page - 1) * limit
    endIndex = page * limit

    return data[startIndex:endIndex]


def format(pk: str) -> dict:
    order = Order.get(pk)

    return {
        "id": order.pk,
        "product_id": order.product_id,
        "price": round(order.price, 2),
        "fee": round(order.fee, 2),
        "total": round(order.total, 2),
        "quantity": order.quantity,
        "status": order.status.value,
    }


# ---------------------------------------------------------------------- #
# Order Handling
# ---------------------------------------------------------------------- #
def order_completed(order: Order) -> None:
    if settings.USE_STREAMS:
        time.sleep(5)

    order.status = OrderStatus.COMPLETED
    order.save()

    if settings.USE_STREAMS:
        complete_with_streams(order)
    else:
        complete_with_rest_api(order)


def refund_order(order: Order) -> None:
    order.status = OrderStatus.REFUNDED
    order.save()


def complete_with_rest_api(order: Order) -> None:
    url = "%s/%s" % (settings.PRODUCT_API, order.product_id)
    response: httpx.Response = httpx.get(url)
    if response.status_code != status.HTTP_404_NOT_FOUND:
        product = response.json()

        del product["pk"]
        product["quantity"] -= int(order.quantity)

        if product["quantity"] >= 0:
            payload = json.dumps(product)
            httpx.put(url, data=payload)
            return

    refund_order(order)


def complete_with_streams(order: Order) -> None:
    database.xadd("order_completed", jsonable_encoder(order), "*")


# ---------------------------------------------------------------------- #
# Error Handling
# ---------------------------------------------------------------------- #
def not_found_msg(id) -> str:
    return f"Order with ID {id} not found"


def does_not_exist_msg(id) -> str:
    return f"Product with ID {id} doesn't exist. Order cannot be placed"
