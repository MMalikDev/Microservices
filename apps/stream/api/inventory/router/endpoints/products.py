from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from models.products import Product, ProductSchema
from redis_om import NotFoundError
from router import handlers

router = APIRouter()


@router.get("", response_model=List[ProductSchema])
def all(page: int = 1, limit: int = 100) -> JSONResponse:
    data = [handlers.format(pk) for pk in Product.all_pks()]
    content = handlers.pagination(data, page, limit)

    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.post("", response_model=ProductSchema)
def create(product: ProductSchema) -> JSONResponse:
    data = product.model_dump()
    new_product = Product(**data)
    content = new_product.save()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(content),
    )


@router.get("/{pk}", response_model=ProductSchema)
def get(pk: str) -> JSONResponse:
    try:
        content = Product.get(pk)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(content),
        )

    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=handlers.not_found_msg(pk),
        )


@router.put("/{pk}", response_model=ProductSchema)
def put(pk: str, product: ProductSchema) -> JSONResponse:
    try:
        data = Product.get(pk)
        new_data = product.model_dump()
        data.update(**new_data)

        content = data = Product.get(pk)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(content),
        )

    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=handlers.not_found_msg(pk),
        )


@router.delete("/{pk}")
def delete(pk: str) -> Response:
    if not Product.delete(pk):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=handlers.not_found_msg(pk),
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
