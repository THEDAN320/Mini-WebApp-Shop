from datetime import datetime, UTC
from typing import Any

from models.src.modules.orders_goods import OrderGoods
from models.src.repository import BaseRepository
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


def get_search_row_OrderGoodss(
    query: Any,
    search_data: dict[str, Any] | None,
) -> Any:
    if search_data is None:
        query = query.where(OrderGoods.deleted_at == None)  # noqa
    else:
        query = query.where(OrderGoods.deleted_at == None)  # noqa

    return query


def get_ordering_OrderGoodss(
    self: Any,
    query: Any,
    value: str | list[str | list[str]] | None,
    search_data: dict[str, Any] | None = None,
) -> Any:
    if value is None:
        query = query.order_by(OrderGoods.id.desc())
    elif isinstance(value, list):
        for item in value:
            if item == "id__asc":
                query = query.order_by(OrderGoods.id.asc())
            elif item == "id__desc":
                query = query.order_by(OrderGoods.id.desc())

            elif item == "order_id__asc":
                query = query.order_by(OrderGoods.order_id.asc())
            elif item == "order_id__desc":
                query = query.order_by(OrderGoods.order_id.desc())

            elif item == "created_at__asc":
                query = query.order_by(OrderGoods.created_at.asc())
            elif item == "created_at__desc":
                query = query.order_by(OrderGoods.created_at.desc())

            elif item == "updated_at__asc":
                query = query.order_by(OrderGoods.updated_at.asc())
            elif item == "updated_at__desc":
                query = query.order_by(OrderGoods.updated_at.desc())

            elif item == "deleted_at__asc":
                query = query.order_by(OrderGoods.deleted_at.asc())
            elif item == "deleted_at__desc":
                query = query.order_by(OrderGoods.deleted_at.desc())

    return query


class OrderGoodsRepository(BaseRepository[OrderGoods]):
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
        return get_search_row_OrderGoodss(query, search_data)

    def ordering(
        self,
        query: Any,
        value: str | list[str | list[str]] | None,
        search_data: dict[str, Any] | None = None,
    ) -> Any:
        return get_ordering_OrderGoodss(self, query, value, search_data)


OrderGoods_repository = OrderGoodsRepository(OrderGoods)
