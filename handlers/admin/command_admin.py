from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import IDFilter

from keyboards.admin_inline.admin_menu_inkb import admin_menu_inkb

from data.config import cfg_data


async def command_admin(message: types.Message):

    await message.answer(text='Hay admin!', reply_markup=admin_menu_inkb)
    await message.delete()

def register_command_admin(dispatcher: Dispatcher):

    dispatcher.register_message_handler(command_admin,
                                        IDFilter(cfg_data['admin_id']),
                                        commands=['admin'],
                                        state='*'
                                        )
