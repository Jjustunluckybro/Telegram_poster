from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import IDFilter

from keyboards.admin_inline.admin_menu_inkb import admin_menu_inkb

from data.config import cfg_data

from utils.create_utils import data


async def callback_delete_data_table(callback: types.CallbackQuery):
    pass


def register_callback_delete_from_data(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_delete_data_table,
                                               IDFilter(user_id=cfg_data['admin_id']),
                                               state='*'
                                               )
