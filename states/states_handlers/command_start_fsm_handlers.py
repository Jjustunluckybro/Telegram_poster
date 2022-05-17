from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import types

from states.states_classes.StartFSM import StartFSM
from utils.create_utils import data

from keyboards.inline.start_inkb import start_inkb
from keyboards.inline.menu_inkb import menu_inkb
from keyboards.inline.close_inkb import close_inkb
from keyboards.inline.finish_inkb import finish_inkb
from keyboards.inline.set_forwarding_group_inkb import set_forwarding_group_inlb


async def command_start(message: types.Message):
    """
    After command /start
    User has two options:
    1) Start - start initial setup
    2) Skip - skip initial setup and open main menu
    """
    text = 'Hello, to start initial setup choose "Start".'

    await StartFSM.start_initial_setup.set()
    user_id = message.from_user.id
    await data.add_to_data(user_id=user_id, forwarding_group=user_id)
    await message.answer(text=text, reply_markup=start_inkb)
    await message.delete()


async def callback_skip_setup(callback: types.CallbackQuery, state: FSMContext):
    """Skip initial setup from first step"""

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.edit_text(text='Initial setup was skipped', reply_markup=menu_inkb)
    await callback.answer('Initial setup was skipped')


async def callback_start_setup(callback: types.CallbackQuery):
    """Start initial setup from first step"""

    text = "Please forward post from channel you want to add\n When you're done, pleas choose 'Finish'"
    await callback.message.edit_text(text=text, reply_markup=finish_inkb)
    await StartFSM.next()


async def callback_finish(callback: types.CallbackQuery):
    """
    When user finish add channels to read
    Start setting forwarding_group
    """

    text = 'Now, choose group or channel, where i will reply posts for you.'

    await callback.message.edit_text(text=text, reply_markup=set_forwarding_group_inlb)
    await StartFSM.next()
    await callback.answer()


async def callback_finish_setup(callback: types.CallbackQuery, state: FSMContext):
    """When user finish all initial setup, (use cb_finish to)"""
    await state.finish()
    await callback.message.edit_text(text='Initial setup is finished.\n\nMenu', reply_markup=menu_inkb)
    await callback.answer(text='Setup is finished')


# TODO: Photo problem
async def add_readable_channels_initial_setup(message: types.Message):
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

            text = f'Channel: {group_name} successfull added'
            await message.answer(text=text, reply_markup=close_inkb)
            await message.delete()

    except AttributeError:

        await message.answer('Pleas reply message from channel', reply_markup=close_inkb)
        await message.delete()


async def callback_set_fwd_group_this_dialog(callback: types.CallbackQuery):

    text = 'Set this dialog as dialog to forward posts'

    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    await data.set_forwarding_group(user_id=user_id, group_id=chat_id)

    await callback.answer(text=text, show_alert=True)
    await callback.answer()


async def set_forwarding_group(message: types.Message):

    user_id = message.from_user.id
    group_id = message.forward_from_chat.id
    group_name = message.forward_from_chat.title

    if await data.get_forwarding_group(user_id=user_id) == group_id:
        await message.answer(text='This group or channel already set as you group to forward', reply_markup=close_inkb)
        await message.delete()
    else:
        if await data.set_forwarding_group(user_id=user_id, group_id=group_id):
            text = f"{group_name} is new group, where i'll sent your new posts"

            await message.answer(text=text, reply_markup=close_inkb)
            await message.delete()
        else:
            text = """Sorry, i can't send message to this group, please choose another"""
            await message.answer(text=text, reply_markup=close_inkb)
            await message.delete()


def register_start_fsm_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(command_start, commands=['start'], state=None)
    dispatcher.register_callback_query_handler(callback_skip_setup,
                                               Text(equals='cb_skip_setup'),
                                               state=StartFSM.start_initial_setup
                                               )
    dispatcher.register_callback_query_handler(callback_start_setup,
                                               Text(equals='cb_start_setup'),
                                               state=StartFSM.start_initial_setup
                                               )
    dispatcher.register_message_handler(add_readable_channels_initial_setup,
                                        state=StartFSM.add_channels,
                                        content_types=['text', 'photo', 'video']  # TODO: photo etc
                                        )

    dispatcher.register_callback_query_handler(callback_finish,
                                               Text(equals='cb_finish'),
                                               state=StartFSM.add_channels,
                                               )
    dispatcher.register_callback_query_handler(callback_finish_setup,
                                               Text(equals='cb_finish'),
                                               state=StartFSM.add_reply_group
                                               )
    dispatcher.register_callback_query_handler(callback_set_fwd_group_this_dialog,
                                               Text(equals='cb_set_this'),
                                               state=StartFSM.add_reply_group
                                               )
    dispatcher.register_message_handler(set_forwarding_group,
                                        state=StartFSM.add_reply_group,
                                        content_types=['text', 'photo', 'video']  # TODO: photo etc
                                        )
