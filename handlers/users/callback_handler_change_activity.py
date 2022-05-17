from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from utils.create_utils import data


async def callback_change_activity(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await data.change_activity(user_id=user_id)

    if await data.get_activity(user_id=user_id):
        await callback.answer('Activity has been changed!\n\nNow bot is active for you', show_alert=True)
    else:
        await callback.answer('Activity has been changed!\n\nNow bot is not active for you', show_alert=True)


def register_change_activity(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_change_activity,
                                               Text(equals='cb_change_activity'),
                                               state=None
                                               )
