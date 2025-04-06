from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    """States for menu."""

    main = State()
