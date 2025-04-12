from config import get_backend_settings
from core.dal import BaseDAL
from models.src.modules.goods import Good
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import Good_repository
from .schemas import (
    CreateGoodSchema,
    UpdateGoodSchema,
    GoodSchema,
    GoodsListSchema,
    GoodsPaginationSchema,
    GoodsSearchSchema,
)

settings = get_backend_settings()


class GoodDAL(
    BaseDAL[
        Good,
        GoodSchema,
        GoodsListSchema,
        GoodsPaginationSchema,
        CreateGoodSchema,
        UpdateGoodSchema,
        GoodsSearchSchema,
    ]
):
    @staticmethod
    async def get_all(
        db: AsyncSession,
        pagi: GoodsPaginationSchema | None = None,
        search_data: GoodsSearchSchema | None = None,
    ) -> GoodsListSchema:
        pagi_dict = (
            pagi.model_dump(exclude_unset=True) if pagi is not None else None
        )
        search_data_dict = (
            search_data.model_dump(exclude_unset=True)
            if search_data is not None
            else None
        )

        items = await Good_repository.get_multi(
            db,
            pagi=pagi_dict,
            search_data=search_data_dict,
        )
        total = await Good_repository.get_count_multi(
            db, search_data=search_data_dict
        )
        return GoodsListSchema(
            items=TypeAdapter(list[GoodSchema]).validate_python(items),
            total=total,
        )

    @staticmethod
    async def create(db: AsyncSession, data: CreateGoodSchema) -> GoodSchema:
        current_data = data.model_dump()
        item = await Good_repository.create(db, current_data)
        return GoodSchema.model_validate(item)

    @staticmethod
    async def update(
        db: AsyncSession,
        item_id: int,
        data: UpdateGoodSchema,
    ) -> GoodSchema:
        new_data = data.model_dump(exclude_unset=True)
        item = await Good_repository.update(db, item_id, new_data)
        return GoodSchema.model_validate(item)

    @staticmethod
    async def delete(db: AsyncSession, item_id: int) -> int | None:
        return await Good_repository.delete(db, item_id)

    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: int) -> GoodSchema | None:
        item = await Good_repository.get(db, item_id)

        if item is not None:
            return GoodSchema.model_validate(item)
        return None
