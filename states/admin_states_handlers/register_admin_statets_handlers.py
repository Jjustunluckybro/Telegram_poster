from aiogram.dispatcher import Dispatcher
from .test_admin_handler import register_test_mode_handlers


def register_admin_states_handlers(dispatcher: Dispatcher):
    register_test_mode_handlers(dispatcher=dispatcher)
