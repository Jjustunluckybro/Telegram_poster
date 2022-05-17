from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.close_inkb import close_inkb_button

admin_test_mode_button = InlineKeyboardButton(text='Activate test mode', callback_data='acb_test')
admin_delete_data_table = InlineKeyboardButton(text='Delete "Data" bd table', callback_data='acb_del_data')
admin_delete_groups_table = InlineKeyboardButton(text='Delete "groups_names" db table', callback_data='acb_del_groups')

admin_menu_inkb = InlineKeyboardMarkup(row_width=1)
admin_menu_inkb.add(admin_test_mode_button,
                    admin_delete_data_table,
                    admin_delete_groups_table,
                    close_inkb_button
                    )

