from aiogram.dispatcher import Dispatcher

from .command_admin import register_command_admin
from .callback_handler_delete_data_table import register_callback_delete_from_data


def register_handlers_admin(dispatcher: Dispatcher):
    register_command_admin(dispatcher=dispatcher)
    register_command_admin(dispatcher=dispatcher)
