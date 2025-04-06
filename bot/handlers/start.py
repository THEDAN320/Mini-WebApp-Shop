from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode

from states.user import Menu


start_router = Router()


@start_router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager) -> None:
    """/start handler."""
    await dialog_manager.start(
        state=Menu.main,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
