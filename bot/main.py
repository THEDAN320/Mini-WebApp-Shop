import asyncio
import logging
import signal
import sys
from typing import NoReturn

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from handlers import handlers_router
from dialogs import dialogs_router

from config import get_bot_settings


def signal_handler(sig: int, frame: object) -> NoReturn:
    """Stop the bot when the signal is received."""
    logging.info("Bot has stopped!")
    sys.exit(0)


async def main() -> None:
    """Start the bot."""
    signal.signal(signal.SIGINT, signal_handler)
    logging.basicConfig(level=logging.INFO)

    bot_settings = get_bot_settings()
    bot = Bot(token=bot_settings.BOT_TOKEN)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(handlers_router)
    dp.include_router(dialogs_router)

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
