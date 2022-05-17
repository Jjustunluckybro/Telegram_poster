from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

finish_inkb_button = InlineKeyboardButton(text='finish', callback_data='cb_finish')

finish_inkb = InlineKeyboardMarkup(row_width=1)
finish_inkb.add(finish_inkb_button)