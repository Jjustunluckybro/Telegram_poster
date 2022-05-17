from aiogram.dispatcher import Dispatcher

from .buffer_group_incoming_message_handler import register_buffer_group_incoming_message


def register_handlers_buffer_channel(dispatcher: Dispatcher):
    register_buffer_group_incoming_message(dispatcher=dispatcher)
