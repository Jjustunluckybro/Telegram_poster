import asyncio
from aiogram import types
from create_bot import bot

from utils.db_api.DataTool import DataTool


class MediaHandler:
    """
    Singleton class to handle different messages from buffer group into one
    message and send it to the users
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, data: DataTool):
        self.data = data
        self.__group_datatime_messages: dict = {}  # key: tuple(fwd_group_id, fwd_datatime); value: list of messages
        self.__group_datatime_task: dict = {}  # key: tuple(fwd_group_id, fwd_datatime); value: task

    async def process_message(self, message: types.Message):
        print(f'\n**Statr processing message with id: {message.message_id}**')
        group_and_data = await self.get_message_group_id_and_data(message=message)
        await self.__add_to_group_datatime_messages(message=message, group_and_data=group_and_data)

        try:
            task = self.__group_datatime_task[group_and_data]
            task.cancel()
            self.__group_datatime_task[group_and_data] = asyncio.create_task(self.__set_media_group(message=message,
                                                                                                    sleep_delay=5
                                                                                                    ))
        except KeyError:
            self.__group_datatime_task[group_and_data] = asyncio.create_task(self.__set_media_group(message=message,
                                                                                                    sleep_delay=5
                                                                                                    ))

    async def __set_media_group(self, message: types.Message, sleep_delay: float | int):
        try:
            await asyncio.sleep(sleep_delay)
            media = await self.__get_all_media_from_same_post(message=message)
            await self.send_media(media=media, fwd_from_id=message.forward_from_chat.id)
        except asyncio.CancelledError:
            pass

    async def __get_all_media_from_same_post(self, message: types.Message):
        input_media: list = []
        message_group_and_data = await self.get_message_group_id_and_data(message=message)
        messages = self.__group_datatime_messages[message_group_and_data]

        for cycle_message in messages:
            text: str = await self.get_text(message=cycle_message)

            if cycle_message.text:
                return text

            elif cycle_message.photo:
                photo_id = await self.get_photo_id(message=cycle_message)
                input_media.append(types.InputMediaPhoto(media=photo_id, caption=text))
                continue

            elif cycle_message.video:
                video_id = await cycle_message.video.file_id
                input_media.append(types.InputMediaVideo(media=video_id, caption=text))
                continue

            elif cycle_message.document:
                document_id = cycle_message.document.file_id
                input_media.append(types.InputMediaDocument(media=document_id, caption=text))
                continue

            elif cycle_message.video_note:
                video_note_id = cycle_message.video_note.file_id
                input_media.append(types.InputMediaVideo(media=video_note_id, caption=text))
                continue

            elif cycle_message.voice:
                voice_id = cycle_message.voice.file_id
                input_media.append(types.InputMediaAudio(media=voice_id, caption=text))
                continue

            elif cycle_message.animation:
                animation_id = cycle_message.animation.file_id
                input_media.append(types.InputMediaAnimation(media=animation_id, caption=text))
                continue

        self.__group_datatime_messages.pop(message_group_and_data)
        self.__group_datatime_task.pop(message_group_and_data)
        return input_media

    async def __add_to_group_datatime_messages(self, message: types.Message, group_and_data: tuple | None = None):
        if group_and_data is None:
            group_and_data = await self.get_message_group_id_and_data(message=message)

        try:
            messages = self.__group_datatime_messages[group_and_data]
            messages.append(message)
            self.__group_datatime_messages[group_and_data] = messages
        except KeyError:
            messages: list = [message]
            self.__group_datatime_messages[group_and_data] = messages

    @staticmethod
    async def get_text(message: types.Message) -> str:
        title = message.forward_from_chat.title
        link = 'Here will be link to channel :)'
        if message.caption:
            text = f'{title}\n\n{message.caption}\n\n{link}'
            return text
        elif message.text:
            text = f'{title}\n\n{message.text}\n\n{link}'
            return text
        else:
            return ''

    @staticmethod
    async def get_message_group_id_and_data(message: types.Message) -> tuple:
        group_id = message.forward_from_chat.id
        datatime = message.forward_date
        group_and_data = tuple((group_id, datatime))
        return group_and_data

    @staticmethod
    async def get_photo_id(message: types.Message):
        photo = message.photo
        file_id = photo[0]['file_id']
        return file_id

    async def send_media(self, media, fwd_from_id, delay: int | float = 0.05):
        """
        Sends a message to all active users following this channel
        :param fwd_from_id: From what channel was original post
        :param media: Media or text from original post
        :param delay: Delay between sending messages. Must be no more than 30 sent messages per second,
        so telegram doesn't give mute
        """

        users = await self.data.get_all_active_subscribers_and_forwarding_group(group_id=fwd_from_id)

        if users is None:
            return

        if type(media) is list:
            for user, fwd_grop in users.items():
                await bot.send_media_group(chat_id=fwd_grop, media=media)
                await asyncio.sleep(delay)
            return

        elif type(media) is str:
            for user, fwd_grop in users.items():
                await bot.send_message(chat_id=fwd_grop, text=media)
                await asyncio.sleep(delay)
            return

        else:
            raise TypeError('What the heck you give me bro o_O')
