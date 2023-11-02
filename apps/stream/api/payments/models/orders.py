from enum import Enum

from db.setup import database
from pydantic import BaseModel
from redis_om import HashModel


class OrderStatus(Enum):
    PENDING = "pending"
    REFUNDED = "refunded"
    COMPLETED = "completed"


class NewOrderSchema(BaseModel):
    product_id: str
    quantity: int


class OrderSchema(BaseModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: OrderStatus


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: OrderStatus

    class Meta:
        database = database
