from aiogram import Router
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import WebApp
from aiogram_dialog.widgets.text import Const

from states.user import Menu

from config import get_bot_settings

bot_settings = get_bot_settings()


menu_window = Window(
    Const("Добро пожаловать в главное меню!"),
    WebApp(
        text=Const("За покупками"),
        url=Const(bot_settings.BACKEND_URL),
    ),
    state=Menu.main,
)

main_menu_dialog = Dialog(menu_window)

dialogs_router = Router()
dialogs_router.include_routers(main_menu_dialog)


__all__ = ["dialogs_router"]
