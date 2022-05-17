from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from keyboards.inline.menu_inkb import menu_inkb


async def handler_command_start(message: types.Message):
    text = 'menu'

    await message.answer(text=text, reply_markup=menu_inkb)
    await message.delete()


async def callback_menu(callback: types.CallbackQuery):

    text = 'menu'

    await callback.message.edit_text(text=text, reply_markup=menu_inkb)
    await callback.answer()


def register_handler_command_start(dispatcher: Dispatcher):
    dispatcher.register_message_handler(handler_command_start,
                                        commands='menu',
                                        state=None
                                        )
    dispatcher.register_callback_query_handler(callback_menu,
                                               Text(equals='cb_menu'),
                                               state=None
                                               )
