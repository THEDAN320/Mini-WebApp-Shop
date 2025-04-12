from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .dal import OrderDAL
from .schemas import (
    CreateOrderSchema,
    UpdateOrderSchema,
    OrderSchema,
    OrdersListSchema,
    OrdersPaginationSchema,
    OrdersSearchSchema,
)

Orders_router = APIRouter()


@Orders_router.post("/all/", summary="Get all or search Orders")
async def get_all_orders(
    pagi: OrdersPaginationSchema | None = None,
    search_data: OrdersSearchSchema | None = None,
    db: AsyncSession = Depends(get_db),
) -> OrdersListSchema:
    return await OrderDAL.get_all(db, pagi, search_data)


@Orders_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_Order(
    data: CreateOrderSchema,
    db: AsyncSession = Depends(get_db),
) -> OrderSchema:
    return await OrderDAL.create(db, data)


@Orders_router.get("/{item_id}/")
async def get_Order_by_id(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> OrderSchema:
    item = await OrderDAL.get_by_id(db, item_id)
    if item is not None:
        return item
    raise HTTPException(status_code=404, detail="Order not found")


@Orders_router.patch("/{item_id}/")
async def update_Order(
    item_id: int,
    data: UpdateOrderSchema,
    db: AsyncSession = Depends(get_db),
) -> OrderSchema:
    return await OrderDAL.update(db, item_id, data)


@Orders_router.delete("/{item_id}/")
async def delete_Order(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    result = await OrderDAL.delete(db, item_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id: {item_id} does not exist.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
