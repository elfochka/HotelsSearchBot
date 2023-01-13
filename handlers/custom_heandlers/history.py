from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['history'])
def bot_history(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Запрос истории поиска.')
