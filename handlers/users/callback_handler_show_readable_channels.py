from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

from utils.create_utils import data

from keyboards.inline.single_menu_inkb import single_menu_inkb


async def callback_show_readable_channels(callback: types.CallbackQuery):

    user_id = callback.from_user.id
    readable_channels = await data.get_readable_channels(user_id=user_id)

    if readable_channels is None:
        await callback.answer(text='No channels are reading')
    else:
        text = 'There are channels you reading:'
        num = 1
        for channel_id in readable_channels:
            channels = await data.get_group_name_by_id(group_id=int(channel_id))
            text += f'\n{num}. {channels}'
            num += 1

        await callback.message.edit_text(text=text, reply_markup=single_menu_inkb)


def register_show_readable_channels(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_show_readable_channels,
                                               Text(equals='cb_show'),
                                               state=None
                                               )
