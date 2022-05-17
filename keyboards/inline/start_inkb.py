from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_inkb_button = InlineKeyboardButton(text='Start initial setup', callback_data='cb_start_setup')
skip_setup_inkb_button = InlineKeyboardButton(text='Skip initial setup', callback_data='cb_skip_setup')

start_inkb = InlineKeyboardMarkup(row_width=1)
start_inkb.add(start_inkb_button, skip_setup_inkb_button)

