from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .finish_inkb import finish_inkb_button

set_this_dialog_inkb_button = InlineKeyboardButton(text='Set this dialog', callback_data='cb_set_this')

set_forwarding_group_inlb = InlineKeyboardMarkup(row_width=1)
set_forwarding_group_inlb.add(set_this_dialog_inkb_button, finish_inkb_button)

