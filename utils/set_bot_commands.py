import telebot.apihelper
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS


def set_default_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS] + [BotCommand(*i) for i in CUSTOM_COMMANDS]
    )


# def set_custom_commands(bot):
#     bot.set_my_commands(
#         [BotCommand(*i) for i in CUSTOM_COMMANDS]
#     )

# print(telebot.apihelper.set_my_commands())
