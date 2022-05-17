from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import types

from states.states_classes.RemoveFSM import RemoveFSM
from utils.create_utils import data

from keyboards.inline.channel_list_inkb import make_channels_inkb
from keyboards.inline.menu_inkb import menu_inkb


async def callback_remove_readable_channels(callback: types.CallbackQuery):
    text = 'Choose the channel, you want to remove\n\n to stop, choose "Finish"'
    user_id = callback.from_user.id
    user_channels = await data.get_readable_channels(user_id=user_id)

    if user_channels is None:
        await callback.answer(text='No channels are reading')
    else:
        await RemoveFSM.show_inline_keyboard.set()
        inlkb = await make_channels_inkb(channels=user_channels)
        await callback.message.edit_text(text=text, reply_markup=inlkb)


async def callback_finish(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.edit_text(text='Ok\n\nMenu', reply_markup=menu_inkb)
    await callback.answer()


async def callback_remove_channel(callback: types.CallbackQuery, state: FSMContext):
    channel_id = callback.data.split('_')
    channel_id = int(channel_id[-1])
    user_id = callback.from_user.id
    channel_name = await data.get_group_name_by_id(group_id=channel_id)

    await data.remove_chanel_from_readable_channels(user_id=user_id, chanel_id=channel_id)
    await callback.answer(text=f'Channel {channel_name}, success removed')

    try:
        channels = await data.get_readable_channels(user_id=user_id)
        inlkb = await make_channels_inkb(channels=channels)
        await callback.message.edit_reply_markup(reply_markup=inlkb)
    except TypeError:
        await callback.message.edit_reply_markup(reply_markup=menu_inkb)
        await state.finish()
        await callback.answer(text='No more channels is reading')



async def callback_clear(callback: types.CallbackQuery, state: FSMContext):
    """If user choose button 'Clear all channels' on inline keyboard"""

    user_id = callback.from_user.id
    await data.clear_readable_channels(user_id=user_id)
    await callback.answer(text='All readable channels success removed!', show_alert=True)
    await state.finish()
    await callback.message.edit_text(text='Finish setup, No more readable channels\n\nMenu', reply_markup=menu_inkb)


def register_remove_readable_channels_fsm_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_remove_readable_channels,
                                               Text(equals='cb_remove'),
                                               state=None
                                               )
    dispatcher.register_callback_query_handler(callback_finish,
                                               Text(equals='cb_finish'),
                                               state=RemoveFSM.show_inline_keyboard,
                                               )
    dispatcher.register_callback_query_handler(callback_remove_channel,
                                               Text(startswith='del_'),
                                               state=RemoveFSM.show_inline_keyboard
                                               )
    dispatcher.register_callback_query_handler(callback_clear,
                                               Text(equals='cb_clear'),
                                               state=RemoveFSM.show_inline_keyboard
                                               )
