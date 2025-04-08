from datetime import datetime

from core.schemas import BaseSchema, PaginationSchema
from pydantic import field_validator


class GoodSchema(BaseSchema):
    id: int
    article: str
    name: str
    price: float
    count: int
    url: str
    type: str
    description: str

    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    @field_validator("created_at", "updated_at", "deleted_at")
    @classmethod
    def convert_datetime_to_str(cls, v: datetime | None) -> str | None:
        if v is not None:
            return v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return v


class CreateGoodSchema(BaseSchema):
    article: str
    name: str
    price: float
    count: int
    url: str
    type: str
    description: str


class UpdateGoodSchema(BaseSchema):
    article: str
    name: str
    price: float
    count: int
    url: str
    type: str
    description: str


class DeleteGoodSchema(BaseSchema):
    id: int


class GoodsListSchema(BaseSchema):
    total: int
    items: list[GoodSchema]


class GoodsPaginationSchema(PaginationSchema):
    pass
