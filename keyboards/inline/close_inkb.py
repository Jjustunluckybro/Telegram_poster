from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


close_inkb_button = InlineKeyboardButton(text='Close', callback_data='cb_close')

close_inkb = InlineKeyboardMarkup(row_width=1)
close_inkb.add(close_inkb_button)
