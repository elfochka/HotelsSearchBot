from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['bestdeal'])
def bot_bestdeal(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Запрос лучшего предложения.')
