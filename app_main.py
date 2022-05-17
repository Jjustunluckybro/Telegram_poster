from aiogram import executor
from create_bot import dp
import handlers
from states.states_handlers.register_states_handlers import register_states_handlers


def on_startup():

    handlers.register_handlers.register_handlers(dispatcher=dp)
    register_states_handlers(dispatcher=dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup()
                           )
