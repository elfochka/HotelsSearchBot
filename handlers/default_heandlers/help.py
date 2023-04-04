from telebot.types import Message
from config_data.config import CUSTOM_COMMANDS
from loader import bot
from hotlog import hotels_log


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Ловим команду help и выдаем список кастомных команд
    :param message:
    :return: (None)
    """
    try:
        text = [f'/{command} - {desk}' for command, desk in CUSTOM_COMMANDS]
        bot.reply_to(message, '\n'.join(text))
    except Exception as e:
        hotels_log.logger.exception(e)
