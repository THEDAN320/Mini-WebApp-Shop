from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.users.router import Users_router
from routers.goods.router import Goods_router
from routers.orders.router import Orders_router
from routers.order_goods.router import OrderGoodss_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def create_backend_app() -> FastAPI:
    app = FastAPI(title="Backend service", lifespan=lifespan)

    v1_api_router = APIRouter()
    v1_api_router.include_router(Users_router, prefix="/users", tags=["Users"])
    v1_api_router.include_router(Goods_router, prefix="/goods", tags=["Goods"])
    v1_api_router.include_router(
        Orders_router, prefix="/orders", tags=["Orders"]
    )
    v1_api_router.include_router(
        OrderGoodss_router, prefix="/order_goods", tags=["OrderGoods"]
    )
    app.include_router(v1_api_router, prefix="/api/v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app_backend = create_backend_app()
