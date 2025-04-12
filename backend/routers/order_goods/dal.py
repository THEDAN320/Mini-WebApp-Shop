from config import get_backend_settings
from core.dal import BaseDAL
from models.src.modules.orders_goods import OrderGoods
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import OrderGoods_repository
from .schemas import (
    CreateOrderGoodsSchema,
    UpdateOrderGoodsSchema,
    OrderGoodsSchema,
    OrderGoodssListSchema,
    OrderGoodssPaginationSchema,
    OrderGoodssSearchSchema,
)

settings = get_backend_settings()


class OrderGoodsDAL(
    BaseDAL[
        OrderGoods,
        OrderGoodsSchema,
        OrderGoodssListSchema,
        OrderGoodssPaginationSchema,
        CreateOrderGoodsSchema,
        UpdateOrderGoodsSchema,
        OrderGoodssSearchSchema,
    ]
):
    @staticmethod
    async def get_all(
        db: AsyncSession,
        pagi: OrderGoodssPaginationSchema | None = None,
        search_data: OrderGoodssSearchSchema | None = None,
    ) -> OrderGoodssListSchema:
        pagi_dict = (
            pagi.model_dump(exclude_unset=True) if pagi is not None else None
        )
        search_data_dict = (
            search_data.model_dump(exclude_unset=True)
            if search_data is not None
            else None
        )

        items = await OrderGoods_repository.get_multi(
            db,
            pagi=pagi_dict,
            search_data=search_data_dict,
        )
        total = await OrderGoods_repository.get_count_multi(
            db, search_data=search_data_dict
        )
        return OrderGoodssListSchema(
            items=TypeAdapter(list[OrderGoodsSchema]).validate_python(items),
            total=total,
        )

    @staticmethod
    async def create(
        db: AsyncSession, data: CreateOrderGoodsSchema
    ) -> OrderGoodsSchema:
        current_data = data.model_dump()
        item = await OrderGoods_repository.create(db, current_data)
        return OrderGoodsSchema.model_validate(item)

    @staticmethod
    async def update(
        db: AsyncSession,
        item_id: int,
        data: UpdateOrderGoodsSchema,
    ) -> OrderGoodsSchema:
        new_data = data.model_dump(exclude_unset=True)
        item = await OrderGoods_repository.update(db, item_id, new_data)
        return OrderGoodsSchema.model_validate(item)

    @staticmethod
    async def delete(db: AsyncSession, item_id: int) -> int | None:
        return await OrderGoods_repository.delete(db, item_id)

    @staticmethod
    async def get_by_id(
        db: AsyncSession, item_id: int
    ) -> OrderGoodsSchema | None:
        item = await OrderGoods_repository.get(db, item_id)

        if item is not None:
            return OrderGoodsSchema.model_validate(item)
        return None
