from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from utils.create_utils import data


async def callback_show_activity(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    activity = await data.get_activity(user_id=user_id)
    if activity:
        await callback.answer(text='Bot is active now')
    else:
        await callback.answer(text='Bot is not active now')


def register_show_activity(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_show_activity,
                                               Text(equals='cb_show_activity'),
                                               state=None
                                               )
