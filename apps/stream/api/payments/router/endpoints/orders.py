from typing import List, Union

import httpx
from config.core import settings
from fastapi import APIRouter, HTTPException, status
from fastapi.background import BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from models.orders import NewOrderSchema, Order, OrderSchema, OrderStatus
from redis_om import NotFoundError
from router import handlers

router = APIRouter()


@router.get("", response_model=List[OrderSchema])
def all(page: int = 1, limit: int = 100) -> JSONResponse:
    data = [handlers.format(pk) for pk in Order.all_pks()]
    content = handlers.pagination(data, page, limit)

    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.post("", response_model=OrderSchema)
async def create(
    order: NewOrderSchema,
    background_tasks: BackgroundTasks,
) -> Union[JSONResponse, Response]:
    if order.quantity <= 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    url = "%s/%s" % (settings.PRODUCT_API, order.product_id)
    response: httpx.Response = httpx.get(url)
    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=handlers.does_not_exist_msg(order.product_id),
        )

    product = response.json()
    product_id = product["pk"]
    price = product["price"]

    new_order = Order(
        product_id=product_id,
        price=price,
        fee=price * 0.2,
        total=price * 1.2,
        quantity=order.quantity,
        status=OrderStatus.PENDING,
    )

    content = new_order.save()
    background_tasks.add_task(handlers.order_completed, new_order)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(content),
    )


@router.get("/{pk}", response_model=OrderSchema)
def get(pk: str) -> JSONResponse:
    try:
        content = Order.get(pk)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(content),
        )

    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=handlers.not_found_msg(pk),
        )
