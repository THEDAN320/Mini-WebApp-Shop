from config import get_backend_settings
from core.dal import BaseDAL
from models.src.modules.users import User
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import User_repository
from .schemas import (
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
    UsersListSchema,
    UsersPaginationSchema,
    UsersSearchSchema,
)

settings = get_backend_settings()


class UserDAL(
    BaseDAL[
        User,
        UserSchema,
        UsersListSchema,
        UsersPaginationSchema,
        CreateUserSchema,
        UpdateUserSchema,
        UsersSearchSchema,
    ]
):
    @staticmethod
    async def get_all(
        db: AsyncSession,
        pagi: UsersPaginationSchema | None = None,
        search_data: UsersSearchSchema | None = None,
    ) -> UsersListSchema:
        pagi_dict = (
            pagi.model_dump(exclude_unset=True) if pagi is not None else None
        )
        search_data_dict = (
            search_data.model_dump(exclude_unset=True)
            if search_data is not None
            else None
        )

        items = await User_repository.get_multi(
            db,
            pagi=pagi_dict,
            search_data=search_data_dict,
        )
        total = await User_repository.get_count_multi(
            db, search_data=search_data_dict
        )
        return UsersListSchema(
            items=TypeAdapter(list[UserSchema]).validate_python(items),
            total=total,
        )

    @staticmethod
    async def create(db: AsyncSession, data: CreateUserSchema) -> UserSchema:
        current_data = data.model_dump()
        item = await User_repository.create(db, current_data)
        return UserSchema.model_validate(item)

    @staticmethod
    async def update(
        db: AsyncSession,
        item_id: int,
        data: UpdateUserSchema,
    ) -> UserSchema:
        new_data = data.model_dump(exclude_unset=True)
        item = await User_repository.update(db, item_id, new_data)
        return UserSchema.model_validate(item)

    @staticmethod
    async def delete(db: AsyncSession, item_id: int) -> int | None:
        return await User_repository.delete(db, item_id)

    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: int) -> UserSchema | None:
        item = await User_repository.get(db, item_id)

        if item is not None:
            return UserSchema.model_validate(item)
        return None
