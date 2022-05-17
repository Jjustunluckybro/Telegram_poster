from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import types

from states.states_classes.AddFSM import AddFSM
from utils.create_utils import data

from keyboards.inline.finish_inkb import finish_inkb
from keyboards.inline.close_inkb import close_inkb
from keyboards.inline.menu_inkb import menu_inkb


async def callback_add_readable_channel(callback: types.CallbackQuery):

    text = 'Please forward post from channel you want to add\n if you want stop, pleas choose "Finish"'

    await AddFSM.post.set()
    await callback.message.edit_text(text=text, reply_markup=finish_inkb)


async def callback_finish(callback: types.CallbackQuery, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:
        return
    await state.finish()
    await callback.message.edit_text(text='Ok, stop adding channels\n\nMenu', reply_markup=menu_inkb)
    await callback.answer()


async def handler_add_readable_channel(message: types.Message):

    try:
        group_id = message.forward_from_chat.id
        group_name = message.forward_from_chat.title
        user_id = message.from_user.id
        readable_channels = await data.get_readable_channels(user_id=user_id)

        if (readable_channels is not None) and (str(group_id) in readable_channels):
            await message.answer(text='You already add this channel', reply_markup=close_inkb)
            await message.delete()
        else:
            await data.add_to_groups_names(group_id=group_id, name=group_name)
            await data.add_chanel_to_readable_channels(user_id=user_id, channel_id=group_id)

            await message.answer(text=f'Channel: {group_name} successfully added', reply_markup=close_inkb)

    except AttributeError:

        await message.answer('Pleas reply message from channel', reply_markup=close_inkb)


def register_add_readable_channels_fsm(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_add_readable_channel,
                                               Text('cb_add'),
                                               state=None
                                               )
    dispatcher.register_callback_query_handler(callback_finish,
                                               Text('cb_finish'),
                                               state=AddFSM.post
                                               )
    dispatcher.register_message_handler(handler_add_readable_channel,
                                        state=AddFSM,
                                        content_types=['text', 'photo', 'video'] # TODO: Add Other content types
                                        )
