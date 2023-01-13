from telebot.types import Message
from config_data.config import CUSTOM_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    text = [f'/{command} - {desk}' for command, desk in CUSTOM_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
