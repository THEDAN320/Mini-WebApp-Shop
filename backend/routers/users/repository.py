from datetime import datetime, UTC
from typing import Any

from models.src.modules.users import User
from models.src.repository import BaseRepository
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


def get_search_row_Users(
    query: Any,
    search_data: dict[str, Any] | None,
) -> Any:
    if search_data is None:
        query = query.where(User.deleted_at == None)  # noqa
    else:
        query = query.where(User.deleted_at == None)  # noqa

    return query


def get_ordering_Users(
    self: Any,
    query: Any,
    value: str | list[str | list[str]] | None,
    search_data: dict[str, Any] | None = None,
) -> Any:
    if value is None:
        query = query.order_by(User.id.desc())
    elif isinstance(value, list):
        for item in value:
            if item == "id__asc":
                query = query.order_by(User.id.asc())
            elif item == "id__desc":
                query = query.order_by(User.id.desc())

            elif item == "name__asc":
                query = query.order_by(User.username.asc())
            elif item == "name__desc":
                query = query.order_by(User.username.desc())

            elif item == "created_at__asc":
                query = query.order_by(User.created_at.asc())
            elif item == "created_at__desc":
                query = query.order_by(User.created_at.desc())

            elif item == "updated_at__asc":
                query = query.order_by(User.updated_at.asc())
            elif item == "updated_at__desc":
                query = query.order_by(User.updated_at.desc())

            elif item == "deleted_at__asc":
                query = query.order_by(User.deleted_at.asc())
            elif item == "deleted_at__desc":
                query = query.order_by(User.deleted_at.desc())

    return query


class UserRepository(BaseRepository[User]):
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
        return get_search_row_Users(query, search_data)

    def ordering(
        self,
        query: Any,
        value: str | list[str | list[str]] | None,
        search_data: dict[str, Any] | None = None,
    ) -> Any:
        return get_ordering_Users(self, query, value, search_data)


User_repository = UserRepository(User)
