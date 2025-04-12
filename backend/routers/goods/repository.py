from datetime import datetime, UTC
from typing import Any

from models.src.modules.goods import Good
from models.src.repository import BaseRepository
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


def get_search_row_Goods(
    query: Any,
    search_data: dict[str, Any] | None,
) -> Any:
    if search_data is None:
        query = query.where(Good.deleted_at == None)  # noqa
    else:
        query = query.where(Good.deleted_at == None)  # noqa

    return query


def get_ordering_Goods(
    self: Any,
    query: Any,
    value: str | list[str | list[str]] | None,
    search_data: dict[str, Any] | None = None,
) -> Any:
    if value is None:
        query = query.order_by(Good.id.desc())
    elif isinstance(value, list):
        for item in value:
            if item == "id__asc":
                query = query.order_by(Good.id.asc())
            elif item == "id__desc":
                query = query.order_by(Good.id.desc())

            elif item == "article__asc":
                query = query.order_by(Good.article.asc())
            elif item == "article__desc":
                query = query.order_by(Good.article.desc())

            elif item == "name__asc":
                query = query.order_by(Good.name.asc())
            elif item == "name__desc":
                query = query.order_by(Good.name.desc())

            elif item == "price__asc":
                query = query.order_by(Good.price.asc())
            elif item == "price__desc":
                query = query.order_by(Good.price.desc())

            elif item == "type__asc":
                query = query.order_by(Good.type.asc())
            elif item == "type__desc":
                query = query.order_by(Good.type.desc())

            elif item == "created_at__asc":
                query = query.order_by(Good.created_at.asc())
            elif item == "created_at__desc":
                query = query.order_by(Good.created_at.desc())

            elif item == "updated_at__asc":
                query = query.order_by(Good.updated_at.asc())
            elif item == "updated_at__desc":
                query = query.order_by(Good.updated_at.desc())

            elif item == "deleted_at__asc":
                query = query.order_by(Good.deleted_at.asc())
            elif item == "deleted_at__desc":
                query = query.order_by(Good.deleted_at.desc())

    return query


class GoodRepository(BaseRepository[Good]):
    async def delete(self, db: AsyncSession, item_id: int) -> int | None:
        current_timestamp = datetime.now(UTC)
        data = {"deleted_at": current_timestamp}
        query = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(data)
            .returning(self.model.id)
        )
        result = await db.execute(query)
        await db.commit()
        return result.scalars().first()

    def search_query(
        self, query: Any, search_data: dict[str, Any] | None
    ) -> Any:
        return get_search_row_Goods(query, search_data)

    def ordering(
        self,
        query: Any,
        value: str | list[str | list[str]] | None,
        search_data: dict[str, Any] | None = None,
    ) -> Any:
        return get_ordering_Goods(self, query, value, search_data)


Good_repository = GoodRepository(Good)
