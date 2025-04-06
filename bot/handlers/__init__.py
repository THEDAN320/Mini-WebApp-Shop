from aiogram import Router

from .start import start_router


handlers_router = Router()
handlers_router.include_router(start_router)


__all__ = ["handlers_router"]
