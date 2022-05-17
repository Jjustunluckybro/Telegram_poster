from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_inkb_button = InlineKeyboardButton(text='Menu', callback_data='cb_menu')

single_menu_inkb = InlineKeyboardMarkup(row_width=1)
single_menu_inkb.add(menu_inkb_button)
