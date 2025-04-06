from typing import Generic, Type, TypeVar

from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from models.src.repository import BaseRepository
from models.src.models import Base
from .schemas import BaseSchema

ModelType = TypeVar("ModelType", bound=Base)
ModelSchemaType = TypeVar("ModelSchemaType", bound=BaseSchema)
ModelListSchemaType = TypeVar("ModelListSchemaType", bound=BaseSchema)
ModelPaginationSchemaType = TypeVar(
    "ModelPaginationSchemaType", bound=BaseSchema
)
ModelCreateSchemaType = TypeVar("ModelCreateSchemaType", bound=BaseSchema)
ModelUpdateSchemaType = TypeVar("ModelUpdateSchemaType", bound=BaseSchema)
ModelSearchSchema = TypeVar("ModelSearchSchema", bound=BaseSchema)


class BaseDAL(
    Generic[
        ModelType,
        ModelSchemaType,
        ModelListSchemaType,
        ModelPaginationSchemaType,
        ModelCreateSchemaType,
        ModelUpdateSchemaType,
        ModelSearchSchema,
    ]
):
    def __init__(
        self,
        model: Type[ModelType],
        repository: Type[BaseRepository[ModelType]],
        model_schema: Type[ModelSchemaType],
        model_list_schema: Type[ModelListSchemaType],
    ) -> None:
        self.model = model
        self.repository = repository(self.model)
        self.model_schema = model_schema
        self.model_list_schema = model_list_schema

    async def get_all(
        self,
        db: AsyncSession,
        pagi: ModelPaginationSchemaType | None = None,
        search_data: ModelSearchSchema | None = None,
    ) -> ModelListSchemaType:
        pagi_dict = (
            pagi.model_dump(exclude_unset=True) if pagi is not None else None
        )
        search_data_dict = (
            search_data.model_dump(exclude_unset=True)
            if search_data is not None
            else None
        )

        items = await self.repository.get_multi(
            db, pagi=pagi_dict, search_data=search_data_dict
        )
        total = await self.repository.get_count_multi(
            db, search_data=search_data_dict
        )
        validated_items = TypeAdapter(list[ModelSchemaType]).validate_python(
            items
        )
        return self.model_list_schema.model_validate(
            {
                "items": validated_items,
                "total": total,
            }
        )

    async def create(
        self, db: AsyncSession, data: ModelCreateSchemaType
    ) -> ModelSchemaType:
        current_data = data.model_dump()
        item = await self.repository.create(db, current_data)
        return self.model_schema.model_validate(item)

    async def update(
        self, db: AsyncSession, item_id: int, data: ModelUpdateSchemaType
    ) -> ModelSchemaType:
        new_data = data.model_dump(exclude_unset=True)
        item = await self.repository.update(db, item_id, new_data)
        return self.model_schema.model_validate(item)

    async def delete(self, db: AsyncSession, item_id: int) -> int | None:
        return await self.repository.delete(db, item_id)

    async def get_by_id(
        self, db: AsyncSession, item_id: int
    ) -> ModelSchemaType | None:
        item = await self.repository.get(db, item_id)
        if item is not None:
            return self.model_schema.model_validate(item)
        return None
