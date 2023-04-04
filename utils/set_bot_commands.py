from telebot.types import BotCommand
import handlers
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS
# from handlers import custom_heandlers, default_heandlers
# from telebot.types import Message
from loader import bot
# from states.request_data import UserSearchParam


def set_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS] + [
            BotCommand(*i) for i in CUSTOM_COMMANDS]
    )
