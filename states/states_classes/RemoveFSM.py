from aiogram.dispatcher.filters.state import StatesGroup, State


class RemoveFSM(StatesGroup):
    show_inline_keyboard = State()
