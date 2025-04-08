from datetime import datetime

from app.routers.goods.schemas import GoodSchema
from app.routers.orders.schemas import OrderSchema
from core.schemas import BaseSchema, PaginationSchema
from pydantic import field_validator


class OrderGoodsSchema(BaseSchema):
    id: int
    order_id: int
    good_id: int
    count: int
    price: float

    order: OrderSchema
    good: GoodSchema

    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    @field_validator("created_at", "updated_at", "deleted_at")
    @classmethod
    def convert_datetime_to_str(cls, v: datetime | None) -> str | None:
        if v is not None:
            return v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return v


class CreateOrderGoodsSchema(BaseSchema):
    user_id: int
    good_id: int
    count: int


class UpdateOrderGoodsSchema(BaseSchema):
    count: int
    price: float


class DeleteOrderGoodsSchema(BaseSchema):
    id: int


class OrderGoodssListSchema(BaseSchema):
    total: int
    items: list[OrderGoodsSchema]


class OrderGoodssPaginationSchema(PaginationSchema):
    pass
