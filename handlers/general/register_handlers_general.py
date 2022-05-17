from aiogram.dispatcher import Dispatcher

from . import callback_handler_close


def register_handlers_general(dispatcher: Dispatcher):
    callback_handler_close.register_handlers_callback_close(dispatcher=dispatcher)