from aiogram.dispatcher import Dispatcher

from .handler_command_menu import register_handler_command_start
from .callback_handler_change_activity import register_change_activity
from .callback_handler_show_activity import register_show_activity
from .callback_handler_show_readable_channels import register_show_readable_channels


def register_handlers_users(dispatcher: Dispatcher):
    register_handler_command_start(dispatcher=dispatcher)
    register_change_activity(dispatcher=dispatcher)
    register_show_activity(dispatcher=dispatcher)
    register_show_readable_channels(dispatcher=dispatcher)
