from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from data.config import cfg_data
from os import getenv

# TODO: путь внутри бат файла, поправить
"""Use this line, if you want start project from run.bat file"""
# client_data = ClientData(
#     api_id=getenv('API_ID'),
#     api_hash=getenv('API_HASH'),
#     username=getenv('USERNAME'),
#     bot_token=getenv('BOT_TOKEN'),
#     my_id=getenv('MY_ID')
# )

storage = MemoryStorage()
bot = Bot(token=cfg_data['bot_token'])
dp = Dispatcher(bot=bot, storage=storage)
