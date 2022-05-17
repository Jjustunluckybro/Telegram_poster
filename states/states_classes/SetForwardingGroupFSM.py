from aiogram.dispatcher.filters.state import StatesGroup, State


class ShowForwardingGroup(StatesGroup):
    set_new_group = State()
