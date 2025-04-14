from typing import Any
from fastapi import HTTPException
from config import get_backend_settings
from core.dal import BaseDAL
from models.src.modules.orders import Order
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from routers.order_goods.repository import OrderGoods_repository
from routers.users.repository import User_repository
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

        for item in items:
            item.goods = await OrderGoods_repository.get_multi(  # type: ignore
                db, search_data={"order_id": item.id}
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
        current_data = data.model_dump(exclude_unset=True)

        if current_data.get("user_id") is None:
            raise HTTPException(status_code=400, detail="User ID is required")

        user_id = current_data["user_id"]
        user = await User_repository.get(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_not_paid_orders = await Order_repository.get_multi(
            db, search_data={"user_id": user_id, "is_closed": False}
        )

        if len(user_not_paid_orders) > 0:
            item = user_not_paid_orders[0]
        else:
            item = await Order_repository.create(db, current_data)

        item.goods = await OrderGoods_repository.get_multi(  # type: ignore
            db, search_data={"order_id": item.id}
        )
        return OrderSchema.model_validate(item)

    @staticmethod
    async def update(
        db: AsyncSession,
        item_id: int,
        data: UpdateOrderSchema,
    ) -> OrderSchema:
        new_data = data.model_dump(exclude_unset=True)
        item = await Order_repository.update(db, item_id, new_data)
        item.goods = await OrderGoods_repository.get_multi(  # type: ignore
            db, search_data={"order_id": item_id}
        )
        return OrderSchema.model_validate(item)

    @staticmethod
    async def close(
        db: AsyncSession,
        user_id: int,
    ) -> OrderSchema:
        user = await User_repository.get(db, user_id)
        current_data: dict[str, Any] = {"user_id": user_id}
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        item = await OrderDAL.create(
            db, CreateOrderSchema.model_validate(current_data)
        )

        order_goods = await OrderGoods_repository.get_multi(
            db, search_data={"order_id": item.id}
        )
        price = 0.0
        current_data["sale"] = user.sale
        current_data["is_closed"] = True
        current_data["is_paid"] = False

        for order_good in order_goods:
            price += order_good.price * order_good.count

        current_data["price"] = price
        item = await OrderDAL.update(
            db, item.id, UpdateOrderSchema.model_validate(current_data)
        )
        item.goods = order_goods  # type: ignore
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
