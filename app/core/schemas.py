from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


class PaginationSchema(BaseSchema):
    limit: int
    offset: int
