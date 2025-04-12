from config import get_backend_settings
from core.dal import BaseDAL
from models.src.modules.orders import Order
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import Order_repository
from .schemas import (
    CreateOrderSchema,
    UpdateOrderSchema,
    OrderSchema,
    OrdersListSchema,
    OrdersPaginationSchema,
    OrdersSearchSchema,
)

settings = get_backend_settings()


class OrderDAL(
    BaseDAL[
        Order,
        OrderSchema,
        OrdersListSchema,
        OrdersPaginationSchema,
        CreateOrderSchema,
        UpdateOrderSchema,
        OrdersSearchSchema,
    ]
):
    @staticmethod
    async def get_all(
        db: AsyncSession,
        pagi: OrdersPaginationSchema | None = None,
        search_data: OrdersSearchSchema | None = None,
    ) -> OrdersListSchema:
        pagi_dict = (
            pagi.model_dump(exclude_unset=True) if pagi is not None else None
        )
        search_data_dict = (
            search_data.model_dump(exclude_unset=True)
            if search_data is not None
            else None
        )

        items = await Order_repository.get_multi(
            db,
            pagi=pagi_dict,
            search_data=search_data_dict,
        )
        total = await Order_repository.get_count_multi(
            db, search_data=search_data_dict
        )
        return OrdersListSchema(
            items=TypeAdapter(list[OrderSchema]).validate_python(items),
            total=total,
        )

    @staticmethod
    async def create(db: AsyncSession, data: CreateOrderSchema) -> OrderSchema:
        current_data = data.model_dump()
        item = await Order_repository.create(db, current_data)
        return OrderSchema.model_validate(item)

    @staticmethod
    async def update(
        db: AsyncSession,
        item_id: int,
        data: UpdateOrderSchema,
    ) -> OrderSchema:
        new_data = data.model_dump(exclude_unset=True)
        item = await Order_repository.update(db, item_id, new_data)
        return OrderSchema.model_validate(item)

    @staticmethod
    async def delete(db: AsyncSession, item_id: int) -> int | None:
        return await Order_repository.delete(db, item_id)

    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: int) -> OrderSchema | None:
        item = await Order_repository.get(db, item_id)

        if item is not None:
            return OrderSchema.model_validate(item)
        return None
