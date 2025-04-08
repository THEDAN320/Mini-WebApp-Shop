from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .dal import UserDAL
from .schemas import (
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
    UsersListSchema,
    UsersPaginationSchema,
    UsersSearchSchema,
)

Users_router = APIRouter()


@Users_router.post("/all/", summary="Get all or search Users")
async def get_all_users(
    pagi: UsersPaginationSchema | None = None,
    search_data: UsersSearchSchema | None = None,
    db: AsyncSession = Depends(get_db),
) -> UsersListSchema:
    return await UserDAL.get_all(db, pagi, search_data)


@Users_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_User(
    data: CreateUserSchema,
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    return await UserDAL.create(db, data)


@Users_router.get("/{item_id}/")
async def get_User_by_id(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    item = await UserDAL.get_by_id(db, item_id)
    if item is not None:
        return item
    raise HTTPException(status_code=404, detail="User not found")


@Users_router.patch("/{item_id}/")
async def update_User(
    item_id: int,
    data: UpdateUserSchema,
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    return await UserDAL.update(db, item_id, data)


@Users_router.delete("/{item_id}/")
async def delete_User(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    result = await UserDAL.delete(db, item_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {item_id} does not exist.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
