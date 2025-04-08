from datetime import datetime

from core.schemas import BaseSchema, PaginationSchema
from pydantic import field_validator
from routers.order_goods.schemas import OrderGoodsSchema


class OrderSchema(BaseSchema):
    id: int
    user_id: int
    price: float
    sale: float
    is_paid: bool

    goods: list[OrderGoodsSchema]

    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def convert_datetime_to_str(cls, v: datetime | None) -> str | None:
        if v is not None:
            return v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return v


class CreateOrderSchema(BaseSchema):
    user_id: int


class UpdateOrderSchema(BaseSchema):
    user_id: int
    price: float
    sale: float
    is_paid: bool


class DeleteOrderSchema(BaseSchema):
    id: int


class OrdersListSchema(BaseSchema):
    total: int
    items: list[OrderSchema]


class OrdersPaginationSchema(PaginationSchema):
    pass
