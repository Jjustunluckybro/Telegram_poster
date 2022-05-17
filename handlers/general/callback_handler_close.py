from keyboards.inline.close_inkb import close_inkb
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text


async def callback_close(callback: types.CallbackQuery):
    await callback.message.delete()


def register_handlers_callback_close(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_close,
                                               Text(equals='cb_close'),
                                               state='*'
                                               )
