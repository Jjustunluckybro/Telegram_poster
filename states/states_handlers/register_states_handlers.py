from aiogram.dispatcher import Dispatcher

from .command_start_fsm_handlers import register_start_fsm_handlers
from .add_readable_cannel_fsm_handler import register_add_readable_channels_fsm
from .remove_redable_channel_fsm_handlers import register_remove_readable_channels_fsm_handlers
from .set_forwarding_group_fsm_handlers import register_set_forwarding_group


def register_states_handlers(dispatcher: Dispatcher):
    register_start_fsm_handlers(dispatcher=dispatcher)
    register_add_readable_channels_fsm(dispatcher=dispatcher)
    register_remove_readable_channels_fsm_handlers(dispatcher=dispatcher)
    register_set_forwarding_group(dispatcher=dispatcher)
