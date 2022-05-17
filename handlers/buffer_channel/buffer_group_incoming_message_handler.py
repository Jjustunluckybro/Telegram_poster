from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import IDFilter

from utils.create_utils import data, media_handler
from data.config import cfg_data


async def incoming_message(message: types.Message):

    group_id = message.forward_from_chat.id
    if await data.get_all_active_subscribers(group_id=group_id) is None:
        return
    else:
        await media_handler.process_message(message=message)


def register_buffer_group_incoming_message(dispatcher: Dispatcher):
    dispatcher.register_message_handler(incoming_message,
                                        IDFilter(chat_id=cfg_data['buffer_group_id']),
                                        content_types=['photo', 'video', 'text', 'document', 'vide_note',
                                                       'voice', 'animation']
                                        )
