from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .dal import OrderGoodsDAL
from .schemas import (
    CreateOrderGoodsSchema,
    UpdateOrderGoodsSchema,
    OrderGoodsSchema,
    OrderGoodssListSchema,
    OrderGoodssPaginationSchema,
    OrderGoodssSearchSchema,
)

OrderGoodss_router = APIRouter()


@OrderGoodss_router.post("/all/", summary="Get all or search OrderGoodss")
async def get_all_orders_goodss(
    pagi: OrderGoodssPaginationSchema | None = None,
    search_data: OrderGoodssSearchSchema | None = None,
    db: AsyncSession = Depends(get_db),
) -> OrderGoodssListSchema:
    return await OrderGoodsDAL.get_all(db, pagi, search_data)


@OrderGoodss_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_OrderGoods(
    data: CreateOrderGoodsSchema,
    db: AsyncSession = Depends(get_db),
) -> OrderGoodsSchema:
    return await OrderGoodsDAL.create(db, data)


@OrderGoodss_router.get("/{item_id}/")
async def get_OrderGoods_by_id(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> OrderGoodsSchema:
    item = await OrderGoodsDAL.get_by_id(db, item_id)
    if item is not None:
        return item
    raise HTTPException(status_code=404, detail="OrderGoods not found")


@OrderGoodss_router.patch("/{item_id}/")
async def update_OrderGoods(
    item_id: int,
    data: UpdateOrderGoodsSchema,
    db: AsyncSession = Depends(get_db),
) -> OrderGoodsSchema:
    return await OrderGoodsDAL.update(db, item_id, data)


@OrderGoodss_router.delete("/{item_id}/")
async def delete_OrderGoods(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    result = await OrderGoodsDAL.delete(db, item_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OrderGoods with id: {item_id} does not exist.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
