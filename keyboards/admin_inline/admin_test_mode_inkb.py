from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.close_inkb import close_inkb_button


admin_cancel_test_mode_button = InlineKeyboardButton(text='Cancel test mode', callback_data='acb_cancel_test')

admin_cancel_test_mode_inkb = InlineKeyboardMarkup(row_width=1)
admin_cancel_test_mode_inkb.add(admin_cancel_test_mode_button, close_inkb_button)
