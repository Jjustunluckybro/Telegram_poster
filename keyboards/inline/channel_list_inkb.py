from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.create_utils import data


async def make_channels_inkb(channels: list) -> InlineKeyboardMarkup:
    """
    :param channels: User subscribe channels
    :return: inline keyboard with user channels, row_width = 1
             and two buttons at the end 'Clear all channels' and 'Finish'
             with callbacks: 'cb_clear' and 'cb_finish'
    """

    inkb = InlineKeyboardMarkup(row_width=1)

    for channel in channels:

        channel_name = await data.get_group_name_by_id(group_id=(int(channel)))
        channel_id = channel
        button = InlineKeyboardButton(text=channel_name, callback_data=f'del_{channel_id}')
        inkb.add(button)

    inkb.add(InlineKeyboardButton(text='Clear all channels', callback_data='cb_clear'))
    inkb.add(InlineKeyboardButton(text='Finish', callback_data='cb_finish'))

    return inkb
