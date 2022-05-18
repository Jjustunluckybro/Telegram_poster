from aiogram import executor

from create_bot import dp

import handlers
import states


def on_startup():
    states.register_all_states_handlers.register_all_states_handlers(dispatcher=dp)
    handlers.register_handlers.register_handlers(dispatcher=dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup()
                           )
