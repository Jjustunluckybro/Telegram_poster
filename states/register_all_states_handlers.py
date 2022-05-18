from aiogram.dispatcher import Dispatcher

from .states_handlers.register_states_handlers import register_states_handlers
from .admin_states_handlers.register_admin_statets_handlers import register_admin_states_handlers


def register_all_states_handlers(dispatcher: Dispatcher):
    register_admin_states_handlers(dispatcher=dispatcher)
    register_states_handlers(dispatcher=dispatcher)