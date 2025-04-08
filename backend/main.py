from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, FastAPI
from routers.users.router import Users_router
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def create_backend_app() -> FastAPI:
    app = FastAPI(title="Backend service", lifespan=lifespan)

    v1_api_router = APIRouter()
    v1_api_router.include_router(Users_router, prefix="/users")
    app.include_router(v1_api_router, prefix="/v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app_backend = create_backend_app()
