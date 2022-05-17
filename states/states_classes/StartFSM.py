from aiogram.dispatcher.filters.state import StatesGroup, State


class StartFSM(StatesGroup):
    start_initial_setup = State()
    add_channels = State()
    add_reply_group = State()
