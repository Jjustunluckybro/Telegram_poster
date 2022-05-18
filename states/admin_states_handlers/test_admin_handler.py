from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters import IDFilter, Text
from aiogram import types

from data.config import cfg_data

from states.admin_states_classes.TestFSMAdmin import TestFSMAdmin

from keyboards.admin_inline.admin_menu_inkb import admin_menu_inkb
from keyboards.admin_inline.admin_test_mode_inkb import admin_cancel_test_mode_inkb


async def callback_admin_test_mode(callback: types.CallbackQuery):
    text = 'Test mode active now!'

    await TestFSMAdmin.test.set()
    await callback.message.edit_text(text=text, reply_markup=admin_cancel_test_mode_inkb)


async def callback_cancel_test_mode(callback: types.CallbackQuery, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:
        return
    text = 'Test mode inactive now!'
    await state.finish()
    await callback.message.answer(text=text, reply_markup=admin_menu_inkb)
    await callback.message.delete()


async def handler_message_test_mode(message: types.Message):

    msg = str(message)
    await message.answer(text=msg, reply_markup=admin_cancel_test_mode_inkb)


def register_test_mode_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(callback_admin_test_mode,
                                               Text(equals='acb_test'),
                                               state=None
                                               )
    dispatcher.register_callback_query_handler(callback_cancel_test_mode,
                                               Text(equals='acb_cancel_test'),
                                               state=TestFSMAdmin.test,
                                               )
    dispatcher.register_message_handler(handler_message_test_mode,
                                        content_types=types.ContentType.ANY,
                                        state=TestFSMAdmin.test
                                        )

