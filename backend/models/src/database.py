import logging
from typing import AsyncGenerator

from config import get_backend_settings
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)

settings = get_backend_settings()

async_engine = create_async_engine(settings.DATABASE_URL, future=True)

Session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        try:
            yield session
        except SQLAlchemyError as exc:
            await session.rollback()
            logger.error("Get sqlalchemy error")
            raise exc
