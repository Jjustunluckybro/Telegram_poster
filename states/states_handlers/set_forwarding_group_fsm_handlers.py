from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import types

from states.states_classes.SetForwardingGroupFSM import ShowForwardingGroup
from utils.create_utils import data

from keyboards.inline.set_forwarding_group_inkb import set_forwarding_group_inlb
from keyboards.inline.close_inkb import close_inkb
from keyboards.inline.menu_inkb import menu_inkb


async def callback_set_fwd_group(callback: types.CallbackQuery):

    text = 'Now, choose group or channel, where i will reply posts for you'

    await ShowForwardingGroup.set_new_group.set()
    await callback.message.edit_text(text=text, reply_markup=set_forwarding_group_inlb)


async def callback_finish(callback: types.CallbackQuery, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:
        return
    await state.finish()
    await callback.message.edit_text(text='Setup is finished\n\nMenu', reply_markup=menu_inkb)
    await callback.answer()


async def set_group(message: types.Message):

    user_id = message.from_user.id
    group_id = message.forward_from_chat.id
    group_name = message.forward_from_chat.title

    if await data.get_forwarding_group(user_id=user_id) == group_id:
        await message.answer(text='This group or channel already set as you group to forward', reply_markup=close_inkb)
        await message.delete()
    else:

        if await data.set_forwarding_group(user_id=user_id, group_id=group_id):
            text = f"{group_name} is new group, where i'll sent your new posts."
            await message.answer(text=text, reply_markup=close_inkb)
            await message.delete()
        else:
            text = """Sorry, i can't send message to this group, please choose another"""
            await message.answer(text=text, reply_markup=close_inkb)
            await message.delete()


async def callback_set_this_dialog(callback: types.CallbackQuery):

    text = 'Set this dialog as dialog to forward posts\n\nTo finish setup use key "Finish"'

    user_id = callback.from_user.id
    dialog_id = callback.message.chat.id
    await data.set_forwarding_group(user_id=user_id, group_id=dialog_id)

    await callback.answer(text=text, show_alert=True)
    await callback.answer()


def register_set_forwarding_group(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_set_fwd_group,
                                               Text(equals='cb_set_group'),
                                               state=None
                                               )
    dispatcher.register_callback_query_handler(callback_finish,
                                               Text(equals='cb_finish'),
                                               state=ShowForwardingGroup.set_new_group
                                               )
    dispatcher.register_message_handler(set_group,
                                        state=ShowForwardingGroup.set_new_group,
                                        content_types=['text', 'photo', 'video']  # TODO: Add other content types
                                        )
    dispatcher.register_callback_query_handler(callback_set_this_dialog,
                                               Text(equals='cb_set_this'),
                                               state=ShowForwardingGroup.set_new_group
                                               )
