from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .dal import GoodDAL
from .schemas import (
    CreateGoodSchema,
    UpdateGoodSchema,
    GoodSchema,
    GoodsListSchema,
    GoodsPaginationSchema,
    GoodsSearchSchema,
)

Goods_router = APIRouter()


@Goods_router.post("/all/", summary="Get all or search Goods")
async def get_all_goods(
    pagi: GoodsPaginationSchema | None = None,
    search_data: GoodsSearchSchema | None = None,
    db: AsyncSession = Depends(get_db),
) -> GoodsListSchema:
    return await GoodDAL.get_all(db, pagi, search_data)


@Goods_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_Good(
    data: CreateGoodSchema,
    db: AsyncSession = Depends(get_db),
) -> GoodSchema:
    return await GoodDAL.create(db, data)


@Goods_router.get("/{item_id}/")
async def get_Good_by_id(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> GoodSchema:
    item = await GoodDAL.get_by_id(db, item_id)
    if item is not None:
        return item
    raise HTTPException(status_code=404, detail="Good not found")


@Goods_router.patch("/{item_id}/")
async def update_Good(
    item_id: int,
    data: UpdateGoodSchema,
    db: AsyncSession = Depends(get_db),
) -> GoodSchema:
    return await GoodDAL.update(db, item_id, data)


@Goods_router.delete("/{item_id}/")
async def delete_Good(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    result = await GoodDAL.delete(db, item_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Good with id: {item_id} does not exist.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
