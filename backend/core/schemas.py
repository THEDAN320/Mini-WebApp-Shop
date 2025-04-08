from pydantic import BaseModel


class BaseSchema(BaseModel):
    model_config = {"from_attributes": True}


class PaginationSchema(BaseSchema):
    limit: int
    offset: int
