from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from hotlog import hotels_log


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Ловим команду start и выдаем список дефолтных команд
    :param message:
    :return: (None)
    """
    try:
        text = [f"Привет, {message.from_user.full_name}!"] + \
               [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
        bot.reply_to(message, '\n'.join(text))
    except Exception as e:
        hotels_log.logger.exception(e)
