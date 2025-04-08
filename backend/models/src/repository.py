from typing import Any, Generic, Type, TypeVar

from models.src.models import Base
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository class for database operations.

    This class provides a generic implementation of common database operations
    for SQLAlchemy models. It includes methods for creating, retrieving,
    updating and deleting records.

    Generic Args:
        ModelType:
            A TypeVar bound to Base class representing the SQLAlchemy model

    Attributes:
        model (Type[ModelType]):
            The SQLAlchemy model class this repository handles
    """

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, item_id: int) -> ModelType | None:
        return await db.get(self.model, item_id)

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        pagi: dict[str, Any] | None = None,
        search_data: dict[str, Any] | None = None,
        order_by_value: str | list[str | list[str]] | None = None,
    ) -> list[ModelType]:
        query = select(self.model)
        limit = 20
        offset = 0

        if pagi:
            limit = pagi["limit"]
            offset = pagi["offset"]

        query = query.limit(limit).offset(limit * offset)

        query = self.search_query(query, search_data)

        query = self.ordering(query, order_by_value, search_data)

        res = (await db.execute(query)).scalars().all()
        return list(res)

    async def get_count_multi(
        self,
        db: AsyncSession,
        *,
        search_data: dict[str, Any] | None = None,
    ) -> int:
        query = select(func.count(self.model.id))

        query = self.search_query(query, search_data)

        res = (await db.execute(query)).scalars().all()
        return res[0]

    async def create(
        self, db: AsyncSession, data: dict[str, Any]
    ) -> ModelType:
        new_record = self.model(**data)
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
        return new_record

    async def update(
        self, db: AsyncSession, item_id: int, data: dict[str, Any]
    ) -> ModelType | None:
        query = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(data)
            .returning(self.model)
        )
        result = await db.execute(query)
        await db.commit()
        updated_object = result.scalars().first()
        await db.refresh(updated_object)
        return updated_object

    async def delete(self, db: AsyncSession, item_id: int) -> int | None:
        query = (
            delete(self.model)
            .where(self.model.id == item_id)
            .returning(self.model.id)
        )
        result = await db.execute(query)
        await db.commit()
        return result.scalars().first()

    def search_query(
        self, query: Any, search_data: dict[str, Any] | None
    ) -> Any:
        return query

    def ordering(
        self,
        query: Any,
        value: str | list[str | list[str]] | None,
        search_data: dict[str, Any] | None = None,
    ) -> Any:
        return query.order_by(self.model.id.desc())
