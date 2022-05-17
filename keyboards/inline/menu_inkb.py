from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .close_inkb import close_inkb_button


change_activity_inkb_button = InlineKeyboardButton(text='Change bot activity',
                                                   callback_data='cb_change_activity')
current_activity_inkb_button = InlineKeyboardButton(text='Show current bot activity',
                                                    callback_data='cb_show_activity')
remove_readable_channel_inkb_button = InlineKeyboardButton(text='Remove channel from readable',
                                                           callback_data='cb_remove')
add_readable_channel_inkb_button = InlineKeyboardButton(text='Add new channel to readable channel',
                                                        callback_data='cb_add')
set_forwarding_group_inkb_button = InlineKeyboardButton(text='Set new group to forwarding',
                                                        callback_data='cb_set_group')
show_readable_channels_inkb_button = InlineKeyboardButton(text='Show readable channels',
                                                          callback_data='cb_show')

menu_inkb = InlineKeyboardMarkup(row_width=1)
menu_inkb.add(current_activity_inkb_button,
              change_activity_inkb_button,
              add_readable_channel_inkb_button,
              remove_readable_channel_inkb_button,
              set_forwarding_group_inkb_button,
              show_readable_channels_inkb_button,
              close_inkb_button)
