from datetime import datetime

from routers.goods.schemas import GoodSchema
from core.schemas import BaseSchema, PaginationSchema
from pydantic import field_validator, ConfigDict


class OrderGoodsSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    good_id: int
    count: int
    price: float

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
    count: int | None = None
    price: float | None = None


class DeleteOrderGoodsSchema(BaseSchema):
    id: int


class OrderGoodssListSchema(BaseSchema):
    total: int
    items: list[OrderGoodsSchema]


class OrderGoodssPaginationSchema(PaginationSchema):
    pass


class OrderGoodssSearchSchema(BaseSchema):
    id: int | None = None
    order_id: int | None = None
    good_id: int | None = None
    count: int | None = None
