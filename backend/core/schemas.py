from pydantic import BaseModel


class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {"warnings": False},
    }


class PaginationSchema(BaseSchema):
    limit: int
    offset: int
