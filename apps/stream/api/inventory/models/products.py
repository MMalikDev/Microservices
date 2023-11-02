from db.setup import database
from pydantic import BaseModel
from redis_om import HashModel


class ProductSchema(BaseModel):
    name: str
    price: float
    quantity: int


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = database
