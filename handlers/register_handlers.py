from aiogram.dispatcher import Dispatcher

from . import admin
from . import buffer_channel
from . import general
from . import users


def register_handlers(dispatcher: Dispatcher):
    buffer_channel.register_handlers_buffer_channel.register_handlers_buffer_channel(dispatcher=dispatcher)
    users.register_handlers_users.register_handlers_users(dispatcher=dispatcher)
    admin.register_handlers_admin.register_handlers_admin(dispatcher=dispatcher)
    general.register_handlers_general.register_handlers_general(dispatcher=dispatcher)
